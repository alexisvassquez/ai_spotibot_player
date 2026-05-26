# AudioMIX DSP — Control Plane

**Files:** `audio/dsp/core/control/param_ids.h`, `param_registry.h`  
**Namespace:** `audiomix::control`

The control plane is the system that allows external code — the UI, AudioScript, Juniper2.0 — to change DSP parameters safely without interfering with the audio thread. It has two parts: a set of numeric keys that identify parameters, and a registry that maps human-readable names to those keys.

---

## The Problem It Solves

The audio thread runs in a hard real-time context: it must produce output buffers within a fixed deadline, regardless of what else is happening on the system. This means it cannot:

- Acquire a mutex (might block indefinitely if another thread holds it)
- Allocate memory (could trigger the OS allocator, which takes unpredictable time)
- Do string comparisons (involves heap reads and branching)

This creates a problem for parameter control. A user adjusting a knob in the UI, or AudioScript calling `set("eq.band1.gain", 3.0)`, ultimately needs to reach the audio thread. But the most natural representation of "which parameter" — a string like `"eq.band1.gain"` — is exactly what the audio thread cannot use.

The control plane solves this by separating the non-RT setup step (string → integer key mapping) from the RT audio step (integer key lookup → value application).

---

## ParamID — Core Parameter Enum

**File:** `audio/dsp/core/control/param_ids.h`

`ParamID` is a `uint16_t` enum that assigns a stable integer identity to each known parameter in the system. These are the "first-class" parameters — the ones that will always exist, regardless of which modules are loaded.

```cpp
enum class ParamID : uint16_t {
    // Global
    GainDb = 0,
    GainSmoothingMs,

    // EQ (placeholder, expanding when wiring)
    EqEnabled,
    EqBand1GainDb,
    EqBand1FreqHz,
    EqBand1Q,

    // Clipper
    ClipperEnabled,
    ClipperMode,
    ClipperDriveDb,
    ClipperCeilingDb,
    ClipperMix,
    ClipperSmoothingMs,

    ParamCount   // always last — gives total count
};
```

`toIndex(ParamID)` and `paramCount()` are constexpr helpers for array sizing. Since these IDs are stable integers, they can be used as array indices in lock-free lookup tables on the audio thread with no branching and no memory allocation.

The convention is that core `ParamID` values always fit in the lower 16 bits of a `ParamKey` (defined as `uint32_t`). Dynamic module-registered keys live at `kDynamicBase` (65536) and above.

---

## ParamRegistry — Dynamic Parameter Registration

**File:** `audio/dsp/core/control/param_registry.h`

`ParamRegistry` handles parameters that are not known at compile time — those registered by modules at graph-build time, or by user-loaded extensions. It maps human-readable path strings to `ParamKey` integers.

```cpp
class ParamRegistry {
public:
    ParamKey registerDynamic(const std::string& fullName);
    static constexpr ParamKey toKey(ParamID id) noexcept;
};
```

`registerDynamic("shimmer.wet")` assigns and returns a new `ParamKey` for that name. If the same name is registered twice, the same key is returned (idempotent). Keys start at `kDynamicBase = 65536` and increment from there.

`toKey(ParamID)` converts a static enum value to a `ParamKey` — it is just a cast, since the lower 16 bits of the key space are reserved for `ParamID`. This means static and dynamic params live in the same key space and can be handled uniformly by binding tables.

`ParamRegistry` is **non-RT only**. It uses `std::unordered_map` internally, which allocates. It is only called during graph construction (`registerParameters()`) and never during `process()`.

---

## The Double-Buffered Packet Pattern

While `ParamID` and `ParamRegistry` handle the name-to-key mapping, the actual delivery of new parameter values to the audio thread is handled by a **double-buffered atomic packet** pattern that each stateful module implements independently.

This pattern appears in `EqModule`, `CompressorModule`, and `AscensionReverbModule`. Here is how it works in general:

### Setup

Each module maintains:

- An array of two `CoeffPacket` structs (the double buffer)
- `std::atomic<int> mPacketReadyIndex` — which slot has a new packet (`-1` = none pending)
- `std::atomic<int> mPacketWriteIndex` — which slot the control thread is currently writing to

### Control Thread (non-RT)

When a parameter changes, the control thread:

1. Builds a complete `CoeffPacket` containing all derived values for the new state (e.g. precomputed biquad coefficients, envelope time constants in samples, linear-domain gain values)
2. Writes the packet into the *inactive* slot (the one the audio thread is not currently reading from)
3. Atomically stores the slot index into `mPacketReadyIndex` using `memory_order_release`

```cpp
const int next = 1 - mPacketWriteIndex.load(relaxed);
mPackets[next] = pkt;
mPacketWriteIndex.store(next, relaxed);
mPacketReadyIndex.store(next, release);    // publish
```

The `release` store ensures all writes to the packet are visible to the audio thread before the index store becomes visible.

### Audio Thread (RT)

At the start of each `processMulti()` call, before touching any samples:

```cpp
const int idx = mPacketReadyIndex.exchange(-1, acq_rel);
if (idx >= 0) {
    // consume packet
    mActive = mPackets[idx];
    // set up smoothing deltas toward new target coefficients
}
```

`exchange(-1, acq_rel)` atomically reads the index and sets it back to -1 in one operation, ensuring that even if the control thread publishes again mid-block, the audio thread processes at most one packet per block. The `acquire` side of `acq_rel` pairs with the `release` store from the control thread, guaranteeing the packet data is fully visible.

### Why Precomputed Packets

The packet does not store raw parameter values (like `threshold_db = -18.0`). It stores *derived* values: the exponential envelope coefficients already computed from the time constants, the biquad coefficients already computed from frequency/Q/gain. This moves the expensive math (transcendental functions, filter design formulas) to the control thread where it can afford to take time, keeping the audio thread's work to simple arithmetic.

---

## Current Status and Roadmap

The control plane is at **v1** — a solid foundation with room to grow.

What's in place:

- `ParamID` enum covering Gain and Clipper parameters
- `ParamRegistry` for dynamic module registration
- `GainModule` and `ClipperModule` with `registerParameters()` and `bindParameters()` stubs
- The double-buffered packet pattern in EQ, Compressor, and Reverb

What's coming:

- EQ band parameters wired into `ParamRegistry` (currently placeholder entries in `ParamID`)
- A `ParamBindingTable` that stores `ParamKey → RT-safe setter` mappings, allowing a single dispatch path for all parameter updates
- Expansion to `ShimmerModule`, `DigitalChoir`, and `SubBassIsolation`
- Integration with AudioScript's `setParameter()` calls so that the scripting layer goes through registered keys rather than raw strings at runtime
