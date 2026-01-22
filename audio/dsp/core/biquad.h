// ai_spotibot_player
// AudioMIX
// audio/dsp/core/biquad.h

// Real-time EQ engine up to 10 bands
// Per-channel biquad state
// Per-channel biquad state refers to the independent storage of delay variables
// for each audio channel in a digital biquad filter
// allowing a single set of filter coefficients to process multiple channels independently
// Maintains proper filter performance across stereo/multichannel signals
// Smooth coefficient morphing (over N samples - no clicks)

#pragma once
#include <cmath>

namespace audiomix::dsp {

struct BiquadCoeffs {
    float b0 = 1, b1 = 0, b2 = 0;
    float a1 = 0, a2 = 0;    // a0 normalized to 1
};

struct BiquadState {
    float z1 = 0.0f;
    float z2 = 0.0f;
};

static inline float db_to_lin(float db) {
    return std::pow(10.0f, db / 20.0f);
}

// Transposed Direct Form II (stable + efficient)
// TDF-II - a digital filter structure that implements an IIR filter
// first processes zeros (0) (called feedforward path), then poles (feedback path)
// shares delay lines, which results in fewer states + better numerical perform
// read more: https://ccrma.stanford.edu/~jos/fp/Transposed_Direct_Forms.html
static inline float biquad_process_sample(const BiquadCoeffs& c, BiquadState& s, float x) {
    float y = c.b0 * x + s.z1;
    s.z1 = c.b1 * x - c.a1 * y + s.z2;
    s.z2 = c.b2 * x - c.a2 * y;
    return y;
}

}    // namespace audiomix::dsp
