// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/digital_choir.h

// First module in DSP universe: a harmonic cloud/ensemble that takes stereo in
// downmixes to mono for the voices
// outputs a wide stereo choir with wet/dry control

#pragma once

#include "audio/dsp/core/dsp_module.h"
#include "audio/dsp/core/lfo.h"
#include "audio/dsp/core/delay_line.h"
#include "audio/dsp/core/smoothed_parameter.h"

#include <vector>

namespace audiomix::dsp {

class DigitalChoirModule : public DspModule {
public:
    explicit DigitalChoirModule(int numVoices = 8);

    void prepare(double sampleRate,
                 unsigned int maxBlockSize) override;
    void reset() override;

    void process(const float* inL, const float* inR,
                 float* outL, float* outR,
                 unsigned int numFrames) override;

    void setParameter(const std::string& id, float value) override;

private:
    struct Voice {
        float baseDelayMs = 15.0f;
        float modDepthMs = 5.0f;
        float pan = 0.0f;    // -1..+1
        float gain = 0.3f;
        float vibratoDepthCents = 6.0f;
        float vibratoRateHz = 0.6f;

        SimpleLFO lfo;
        DelayLine delay;
    };

    void buildDefaultLayout();

    int mNumVoices;
    double mSampleRate = 44100.0;
    unsigned int mMaxBlockSize = 512;

    std::vector<Voice> mVoices;

    SmoothedParameter mWet;
    SmoothedParameter mDry;

    // For future: spread, density, brightness, and more :)
};

} // namespace audiomix::dsp
