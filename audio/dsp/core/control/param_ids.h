// ai_spotibot_player
// AudioMIX
// audio/dsp/core/control/param_ids.h
//
// Minimal small starter ID list
// Included a global ParamID plus a few basics
// Not the final API surface - bootstrap spine
// v1 :)

#pragma once
#include <cstdint>

namespace audiomix::control {

    // Small starter ID list at first
    // Adding more as we wire modules
    // IDs are RT-facing keys (no strings in the audio callback)
enum class ParamID : uint16_t {
    // Global / engine-level
    GainDb = 0;          // dB gain for GainModule
    GainSmootingMs,      // external control of smoothing

    // EQ
    // Mostly placeholder, will expand when wiring EQ
    EqEnabled,           // 0/1
    EqBand1GainDb,
    EqBand1FreqHz,
    EqBand1Q,

    ParamCount           // always last
};

constexpr uint16_t toIndex(ParamID id) noexcept {
    return static_cast<uint16_t>(id);
}

constexpr uint16_t paramCount() noexcept {
    return static_cast<uint16_t>(ParamID::ParamCount);
}

} // namespace audiomix::control
