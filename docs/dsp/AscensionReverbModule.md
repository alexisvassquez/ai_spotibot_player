# AscensionReverbModule — 8-line Feedback Delay Network (FDN) reverb

> Informational on the AscensionReverbModule. Please refer to `audio/dsp/modules/ascension_reverb.h`

An FDN reverb works by routing audio through N delay lines whose outputs are mixed through a feedback matrix and fed back into their own inputs.
Over time, the exponentially-decaying feedback creates the dense reflective tail we hear as reverberation.

---

## Signal Flow

```cpp
Stereo Input (L, R)
      │
      ▼
  Pre-delay (stereo)         ← onset separation before reverb begins
      │
      ▼
Downmix to mono              ← FDN takes a single excitation signal
      │
      ▼
┌──────────────────────────────────────────────────┐
│                   FDN Core (8 lines)              │
│  y[0..7]  = read delay line outputs              │
│  v[0..7]  = Hadamard8(y)    ← feedback matrix    │
│  damp[i]  = α·damp + (1-α)·v[i]  ← HF absorb   │
│  write[i] = lineGain[i] · damp[i] + mono         │
└──────────────────────────────────────────────────┘
      │
      ▼
M/S width encode             ← even lines → L, odd lines → R
      │
      ▼
Wet/dry blend
      │
      ▼
Stereo Output (L, R)
```

---

## Design choices and why

1. **Mixing matrix** — Normalized 8×8 Hadamard (Walsh-Hadamard transform).
A unitary (energy-preserving) matrix means the network cannot accumulate energy and self-oscillate. The Hadamard transform is also `O(N log N)`, making it cheaper than a full dense matrix at `N=8`.

    - The fast Walsh-Hadamard transform (FWHT) applies the Hadamard matrix in `O(N log N)` butterfly operations — no explicit matrix storage needed.
    - Normalization by `1/√8` makes the transform unitary (energy-preserving).
    - Butterfly structure: for each pass of lengths `[1, 2, 4]`, adjacent pairs `(u, w)` become `(u+w, u-w)`, then the whole array is scaled by `1/√8 ≈ 0.35355`.

2. **Delay line lengths** — Eight prime-ish values `(29, 37, 43, 53, 59, 71, 79, 89 ms)` scaled by a user-controlled "size" parameter. Mutual coprimality breaks up periodic comb filtering and creates a denser, more diffuse tail.

    - If two lines shared a common factor, their interactions would reinforce certain frequencies, producing a metallic or pitched coloration in the tail. Coprime lengths spread resonances evenly across the spectrum.
    - Scaling by `size` (range 0.1–4.0) lets the same algorithm simulate a tight room or a large hall without changing the coprime relationships.
    - Buffer allocation: `ceil(0.09 × 4.2 × sampleRate) + 16` — sized for the longest line (89 ms) at max size (4.0) at up to 192 kHz.

3. **Per-line gain** — Computed from the T60 decay time and each line's length: `g_i = 10^( -3 × d_i / (T60 × sr) )`
After T60 seconds each line has looped `T60×sr/d_i` times. The total attenuation is `g_i^(T60×sr/d_i) = 10^-3 = -60 dB` by construction.

    - Shorter lines cycle more often, so they get a higher per-pass gain to achieve the same T60 as longer lines. The formula accounts for this per-line automatically.
    - This is recomputed on every `setParams()` call, so T60 and room size can change in real time without manual gain recalculation.

4. **HF damping** — One-pole lowpass `(α = exp(-2π·fc/sr))` on the feedback path of each line. As damping rises the cutoff sweeps from 20 kHz down to 300 Hz, simulating air absorption and soft room materials. Applied after the gain so the T60 math stays clean. Logarithmic sweep feels musical and matches perceptual expectations.

    - The sweep formula: `fc = 20000 × (300/20000)^damping`. At `damping=0`, fc=20 kHz (bright). At `damping=1`, fc=300 Hz (dark/absorptive).
    - Applying damping after gain keeps the T60 calculation valid — the energy bookkeeping only depends on the gain stage.
    - The one-pole filter per line (`mDampState[i]`) has its own state, so each delay line absorbs HF independently.

5. **Pre-delay** — Separate stereo circular buffer (0–100 ms) before the FDN input. Separates the direct sound from the reverb onset, giving the mix more depth.

    - FDN lines: longest base delay `(89 ms) × max size (4.0)` at up to 192 kHz
    - `89ms × 4.0 × 192000 Hz ≈ 68352 samples` — round up with headroom
    - Pre-delay buffer: `ceil(0.105 × sampleRate) + 16` — 105 ms of headroom with rounding margin.
    - Pre-delay is stereo (two independent circular buffers), preserving the left/right character of the dry signal before it enters the mono FDN.

6. **Stereo output** — Even-indexed delay lines feed the Left contribution; odd-indexed feed the Right contribution. A simple M/S (mid/side) encode controlled by "width" sweeps from mono (width=0) to fully decorrelated (width=1) with stable loudness.

    - M/S stands for Mid/Side recording and processing.
    - It involves separating a stereo track into a "Mid" channel (the center elements like lead vocals and kick drums) and a "Side" channel (the wide spatial elements like reverb and cymbals) to be EQ'd or compressed independently.
    - Because all 8 lines have different lengths, the even and odd groups are already time-decorrelated — the stereo width comes from natural arrival-time differences, not from artificial pitch shifting or noise injection.
    - Encode: `mid = 0.5×(wetL+wetR)`, `side = 0.5×(wetL-wetR)`, then `outL = mid + width×side`, `outR = mid - width×side`.

7. **Threading model** — Same double-buffered atomic packet pattern as `EqModule` and `CompressorModule`. Control thread builds a `RvbPacket` in `setParams()` and publishes it via atomic index. Audio thread consumes at block boundary, then runs sample by sample with no allocation or locking.

    - `setParams()` precomputes everything expensive off the audio thread: delay lengths in samples, per-line gains, the damping coefficient. The audio thread only does the cheap per-sample work.
    - `wet` and `width` are delivered to the audio thread via `SmoothedParameter` targets, avoiding zipper noise when those values change during playback.
    - See [ControlPlane.md](./ControlPlane.md) for the full double-buffer pattern explanation.

---

## ReverbParams reference

| Parameter | Default | Range | Description |
| --- | --- | --- | --- |
| `pre_delay_ms` | 20 ms | 0–100 ms | Onset gap between dry signal and reverb tail |
| `decay_s` | 2.5 s | 0.1–12 s | T60: time for reverb to fall by 60 dB |
| `size` | 1.2 | 0.1–4.0 | Room size — scales all delay line lengths |
| `damping` | 0.55 | 0–1 | HF absorption (0 = bright/live, 1 = dark/dead) |
| `wet` | 0.25 | 0–1 | Wet/dry mix |
| `width` | 1.0 | 0–1 | Stereo decorrelation amount |
| `sample_rate` | 44100 | — | Used for coefficient computation (informational) |

AudioScript string IDs for `setParameter()`: `"wet"`, `"decay"`, `"size"`, `"dampening"`, `"pre_delay_ms"`, `"width"`.
