# AudioMIX DSP — Core Infrastructure

**Files:** `audio/dsp/core/dsp_module.h`, `dsp_chain.h`, `process_spec.h`, `process_context.h`  
**Namespace:** `audiomix::dsp`

This document covers the four structural pieces that every DSP module and the processing pipeline depend on. None of these classes do signal processing themselves — they define the contracts and plumbing that everything else plugs into.

---

## DspModule

**File:** `audio/dsp/core/dsp_module.h`

`DspModule` is the abstract base class for every effect in AudioMIX. All modules — `EqModule`, `CompressorModule`, `AscensionReverbModule`, and the rest — inherit from it and override its virtual methods.

### Interface

```cpp
class DspModule {
public:
    virtual void prepare(double sampleRate, unsigned int maxBlockSize) = 0;
    virtual void reset() = 0;
    virtual void process(const float* inL, const float* inR,
                         float* outL, float* outR,
                         unsigned int numFrames) = 0;

    virtual void processMulti(const float* const* inputs,
                              float* const* outputs,
                              unsigned int numChannels,
                              unsigned int numFrames);

    virtual void registerParameters(control::ParamRegistry& registry) {}
    virtual void bindParameters(control::ParamBindingTable& bindings) {}
    virtual void setParameter(const std::string& id, float value) {}
};
```

### How It Works

**`prepare(sampleRate, maxBlockSize)`** is called once before audio starts (and again any time the sample rate changes). Modules use this to allocate delay line buffers, pre-compute filter coefficients, and configure internal state. After `prepare()`, the module must be ready to process audio without performing any further allocations.

**`reset()`** clears all internal state — filter histories, delay line contents, envelope followers, smoothing counters — back to silence. It does not deallocate. `DspChain` calls `reset()` immediately after `prepare()`.

**`process()`** is the stereo processing entry point. It receives one block of audio as raw float pointers for left and right channels. `inL`/`inR` may alias `outL`/`outR` (in-place processing is explicitly supported).

**`processMulti()`** is the multichannel entry point. The default implementation in `DspModule` provides a **stereo bridge**: it iterates over channel pairs (0/1, 2/3, etc.) and calls `process()` for each pair. This means a module that only overrides `process()` automatically works correctly in a 4-channel chain without any extra code. Modules that need true multichannel behavior (e.g. a mid/side processor) can override `processMulti()` directly.

The multichannel bridge handles all null-pointer edge cases: if one channel of a pair is missing, it writes silence to the missing output rather than crashing.

### Parameter API

There are two levels of parameter control:

**Legacy string API (`setParameter`)** — accepts a string ID and a float value. This is how AudioScript and Juniper2.0 currently drive modules at runtime (e.g. `setParameter("wet", 0.4f)`). Not real-time safe because strings involve heap memory. Intended for prototyping and scripted control, not for tight audio loops.

**Control plane hooks (`registerParameters` / `bindParameters`)** — the forward-looking RT-safe API. During graph initialization, the control thread calls `registerParameters()` to declare human-readable parameter paths (e.g. `"gain.db"`, `"eq.band1.freq_hz"`). It then calls `bindParameters()` to wire `ParamKey` → RT-safe setter. This path avoids strings on the audio thread entirely. Currently implemented on `GainModule` and `ClipperModule`; expanding to other modules as the control plane matures.

---

## DspChain

**File:** `audio/dsp/core/dsp_chain.h`

`DspChain` owns a sequence of `DspModule` instances and runs them in order on each audio block. It is the only object `main.cpp` needs to interact with at process time.

### How Modules Are Added

```cpp
DspChain chain;
auto* eq  = chain.emplaceModule<EqModule>();
auto* cmp = chain.emplaceModule<CompressorModule>();
auto* rvb = chain.emplaceModule<AscensionReverbModule>();
```

`emplaceModule<T>()` constructs the module in-place, transfers ownership to the chain, and returns a raw pointer for subsequent configuration calls. The chain holds all modules in a `vector<unique_ptr<DspModule>>` — they are destroyed when the chain is destroyed.

### Ping-Pong Buffer Design

Rather than having each module read from and write to a shared in-place buffer (which could corrupt data in complex graphs), the chain maintains two internal temporary buffer sets: `mTmpA` and `mTmpB`. On each process call:

1. The first module reads from the external input and writes into `mTmpA`.
2. The second module reads from `mTmpA` and writes into `mTmpB`.
3. The third module reads from `mTmpB` and writes back into `mTmpA`.
4. This ping-pong continues until the last module, whose output is copied to the caller-supplied output buffers.

This means **no module ever reads from and writes to the same buffer**, even when the caller passes aliased pointers. It also keeps all intermediate buffers pre-allocated — no heap activity at process time.

If the chain has no modules at all, it fast-paths directly from input to output without touching the temp buffers.

### Lazy Prepare

If `processMulti()` is called before `prepare()`, the chain will self-prepare using its current configuration defaults. This is a safety net for test code and late-binding scenarios; in production, `prepare()` should always be called explicitly before the audio thread starts.

### Convenience Wrappers

The chain exposes both entry points that match `DspModule`:

```cpp
chain.process(ctx);                          // via ProcessContext
chain.process(inL, inR, outL, outR, frames); // stereo convenience wrapper
```

---

## ProcessSpec

**File:** `audio/dsp/core/process_spec.h`

`ProcessSpec` carries the static configuration that modules need during `prepare()`. It answers the question: "what kind of audio will I be processing?"

```cpp
struct ProcessSpec {
    double sampleRate   = 44100.0;
    unsigned int maxBlockSize = 0;
    unsigned int numChannels  = 0;
};
```

`sampleRate` is used by filter coefficient calculations, envelope time constants, delay line sizing, and LFO frequency computation — anywhere time-to-samples conversion is needed.

`maxBlockSize` is the largest number of frames that will ever arrive in a single `process()` call. Modules allocate their internal buffers to this size during `prepare()`. If a block arrives that is larger than `maxBlockSize`, the chain hard-clamps it to prevent out-of-bounds writes.

`numChannels` tells the chain how many channel pointers to allocate in its ping-pong buffers. The default is 4 (Master L/R + Booth L/R).

`ProcessSpec` is intentionally minimal and contains no runtime state. It is only used during the setup phase and is never passed to `process()`.

---

## ProcessContext

**File:** `audio/dsp/core/process_context.h`

`ProcessContext` carries the per-block runtime data that the chain needs during `process()`. It answers the question: "what audio am I processing right now?"

```cpp
struct ProcessContext {
    const float* const* inputs  = nullptr;
    float* const*       outputs = nullptr;
    unsigned int numChannels = 0;
    unsigned int numFrames   = 0;
    double sampleRate        = 44100.0;
};
```

`inputs` and `outputs` are pointer-to-pointer arrays, one pointer per channel. The caller owns these buffers — the chain only reads from inputs and writes to outputs, never holding references beyond the call.

`ProcessContext` is designed to grow. Planned additions include `TransportState*` (for BPM-synced effects), `MidiBuffer` (for MIDI-triggered DSP), and `MeterBus` (for exposing level data to the UI and LEDs). Adding these fields to the context struct avoids changing the signature of every module's process method.

---

## How They Work Together

```cpp
main.cpp or performance engine:

  ProcessSpec spec{ 44100.0, 512, 4 };
  chain.prepare(spec);                     // allocates, prepares all modules

  // ... audio loop ...
  ProcessContext ctx;
  ctx.inputs      = hardwareInputBuffers;
  ctx.outputs     = hardwareOutputBuffers;
  ctx.numChannels = 4;
  ctx.numFrames   = 256;

  chain.process(ctx);                      // runs the full module chain
```

`ProcessSpec` lives only in the setup phase. `ProcessContext` lives only in the process phase. The two structs enforce a clean boundary between "what the engine looks like" and "what it is currently doing."
