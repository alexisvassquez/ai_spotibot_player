// ai_spotibot_player
// AudioMIX
// audio/dsp/core/dsp_module.h

// A base class all effects implement
// Multichannel bridge
// Accepts multiple inputs

#pragma once

#include <string>
#include <algorithm>

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

    // Multichannel entry point (default bridge -> stereo)
    // Channels are interleaved as L/R pairs:
    //  0/1 = Master L/R, 2/3 = Booth L/R
    //  will expand for surround sound later
    // Modules that need true multichannel behavior can override
    virtual void processMulti(const float* const* inputs,
                              float* const* outputs,
                              unsigned int numChannels,
                              unsigned int numFrames)
    {
        if (numFrames == 0 || numChannels == 0) return;

        auto zeroIfWritable = [&](float* out) {
            if (out) std::fill(out, out + numFrames, 0.0f);
        };

        // Process in stereo pairs (0,1) (2,3)
        for (unsigned int ch = 0; ch < numChannels; ch += 2) {
            const float* inL = (ch < numChannels) ? inputs[ch] : nullptr;
            const float* inR = (ch + 1 < numChannels) ? inputs[ch + 1] : nullptr;

            float* outL = (ch < numChannels) ? outputs[ch] : nullptr;
            float* outR = (ch + 1 < numChannels) ? outputs[ch + 1] : nullptr;

            // if outputs are missing, nothing to do for this pair
            // continue
            if (!outL && !outR) continue;

            // if one side is missing, write silence to that side (null)
            if (!inL) zeroIfWritable(outL);
            if (!inR) zeroIfWritable(outR);

            // if both inputs exist, run stereo process on this pair
            // if one input is missing, output is already zeroed
            // can still process other side if needed
            // only call process() when both inputs + 1 (min) output exists
            if (inL && inR) {
                process(inL, inR, outL, outR, numFrames);
            } else {
                // if only one input exists, pass through to matching output
                if (inL && outL) std::copy(inL, inL + numFrames, outL);
                if (inR && outR) std::copy(inR, inR + numFrames, outR);
            }
        }
    }

    // Generic param hook so AudioScript/Juniper2.0 can talk to it
    // IDs are arbitrary strings ("wet", "depth", "mix", etc)
    virtual void setParameter(const std::string& id, float value) {
        (void)id;
        (void)value;
    }
};

}  // namespace audiomix::dsp
