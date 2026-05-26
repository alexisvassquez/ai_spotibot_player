# AscensionReverbModule — 8-line Feedback Delay Network (FDN) reverb

> Informational on the AscensionReverbModule. Please refer to `audio/dsp/modules/ascension_reverb.h`

An FDN reverb works by routing audio through N delay lines whose outputs are mixed through a feedback matrix and fed back into their own inputs.
Over time, the exponentially-decaying feedback creates the dense reflective tail we hear as reverberation.

Design choices and why:

1. **Mixing matrix** — Normalized 8×8 Hadamard (Walsh-Hadamard transform).
A unitary (energy-preserving) matrix means the network cannot accumulate energy and self-oscillate. The Hadamard transform is also `O(N log N)`, making it cheaper than a full dense matrix at `N=8`.

    - The fast Walsh-Hadamard transform (FWHT) applies the Hadamard matrix in `O(N log N)` butterfly operations — no explicit matrix storage needed.
    - Normalization by `1/√8` makes the transform unitary (energy-preserving).

2. **Delay line lengths** — Eight prime-ish values `(29, 37, 43, 53, 59, 71, 79, 89 ms)` scaled by a user-controlled "size" parameter. Mutual coprimality breaks up periodic comb filtering and creates a denser, more diffuse tail.

3. **Per-line gain** — Computed from the T60 decay time and each line's length: `g_i = 10^( -3 *d_i / (T60* sr) )`
After T60 seconds each line has looped `T60*sr/d_i` times. The total attenuation is `g_i^(T60*sr/d_i) = 10^-3 = -60 dB` by construction.

4. **HF damping** — One-pole lowpass `(α = exp(-2π·fc/sr))` on the feedback path of each line. As damping rises the cutoff sweeps from 20 kHz down to 300 Hz, simulating air absorption and soft room materials. Applied after the gain so the T60 math stays clean. Logarithmic sweep feels musical and matches perceptual expectations.

5. **Pre-delay** — Separate stereo circular buffer (0–100 ms) before the FDN input. Separates the direct sound from the reverb onset, giving the mix more depth.

    - FDN lines: longest base delay `(89 ms) × max size (4.0)` at up to 192 kHz
    - `89ms * 4.0 * 192000 Hz ≈ 68352 samples` — round up with headroom

6. **Stereo output** — Even-indexed delay lines feed the Left contribution; odd-indexed feed the Right contribution. A simple M/S (mid/side) encode controlled by "width" sweeps from mono (width=0) to fully decorrelated (width=1) with stable loudness.

    - M/S stands for Mid/Side recording and processing.
    - It involves separating a stereo track into a "Mid" channel (the center elements like lead vocals and kick drums) and a "Side" channel (the wide spatial elements like reverb and cymbals) to be EQ'd or compressed independently.

7. **Threading model** — Same double-buffered atomic packet pattern as `EqModule` and `CompressorModule`. Control thread builds a `RvbPacket` in `setParams()` and publishes it via atomic index. Audio thread consumes at block boundary, then runs sample by sample with no allocation or locking.
