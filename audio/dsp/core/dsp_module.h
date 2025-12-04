// ai_spotibot_player
// AudioMIX
// audio/dsp/core/dsp_module.h

// A base class all effects implement

#pragma once

#include <string>

namespace audiomix::dsp {

class DspModule {
public:
    virtual ~DspModule() = default;

    // Called before processing starts (or when sample rate (SR) changes)
    virtual void prepare(double sampleRate,
                         unsigned int maxBlockSize) = 0;

    // Clear internal state (delay lines, filters, etc)
    virtual void reset() = 0;

    // Process one stereo block
    // inL/inR (input left, input r) may alias outL/outR (output left, output right)
    // for in-place processing
    virtual void process(const float* inL, const float* inR,
                         float* outL, float* outR,
                         unsigned int numFrames) = 0;

    // Generic param hook so AudioScript/Juniper2.0 can talk to it
    // IDs are arbitrary strings ("wet", "depth", "mix", etc)
    virtual void setParameter(const std::string& id, float value) {
        (void)id;
        (void)value;
    }
};

}  // namespace audiomix::dsp
