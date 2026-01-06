// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/gain_module.h

// Exposes gain in dB
// Converts dB -> linear once p/block
// Uses smoothed parameter module to smooth linear gain
// Applies to all channel pairs auto via multi process bridge

#pragma once

#include "audio/dsp/core/dsp_module.h"
#include "audio/dsp/core/smoothed_parameter.h"

#include <cmath>
#include <string>

namespace audiomix::dsp {

class GainModule final : public DspModule {
public:
    GainModule() = default;

    void prepare(double sampleRate, unsigned int maxBlockSize) override;
    void reset() override;

    // stereo processing
    // chain's multichannel bridge will call per pair
    void process(const float* inL, const float* inR,
                 float* outL, float* outR,
                 unsigned int numFrames) override;

    void setParameter(const std::string& id, float value) override;

    // convenience API (for C++ callers/tests)
    void setGainDb(float db);
    float getGainDb() const { return mGainDb; }

    void setSmoothingTimeMs(float ms);

private:
    static float dbToLinear(float db) {
        // linear = 10^(dB/20)
        return std::pow(10.0f, db / 20.0f);
    }

private:
    double mSampleRate = 44100.0;
    unsigned int mMaxBlockSize = 0;

    float mGainDb = 0.0f;

    float mSmoothingMs = 20.0f;    // default
    // smooth in linear space to avoid zipper noise
    SmoothedParameter mGainLin;
};

} // namespace audiomix::dsp
