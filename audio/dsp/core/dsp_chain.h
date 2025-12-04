// ai_spotibot_player
// AudioMIX
// audio/dsp/core/dsp_chain.h

// Simple plugin chain that owns modules and runs them in order

#pragma once

#include "audio/dsp/core/dsp_module.h"

#include <memory>
#include <vector>
#include <algorithm>

namespace audiomix::dsp {

class DspChain {
public:
    void setSampleRate(double sr) { mSampleRate = sr; }
    void setMaxBlockSize(unsigned int size) { mMaxBlockSize = size; }

    template <typename ModuleT, typename... Args>
    ModuleT* emplaceModule(Args&&... args) {
        auto mod = std::make_unique<ModuleT>(std::forward<Args>(args)...);
        ModuleT* raw = mod.get();
        mModules.emplace_back(std::move(mod));
        return raw;
    }

    void prepare() {
        if (mSampleRate <= 0.0 || mMaxBlockSize == 0) return;

        mTmpL1.assign(mMaxBlockSize, 0.0f);
        mTmpR1.assign(mMaxBlockSize, 0.0f);
        mTmpL2.assign(mMaxBlockSize, 0.0f);
        mTmpR2.assign(mMaxBlockSize, 0.0f);

        for (auto& m : mModules) {
            m->prepare(mSampleRate, mMaxBlockSize);
            m->reset();
        }
    }

    // Process chain: input -> module1 -> module2 -> ... -> output
    void process(const float* inL, const float* inR,
                 float* outL, float* outR,
                 unsigned int numFrames)
    {
        if (mModules.empty() || numFrames == 0) {
            if (outL && inL) std::copy(inL, inL + numFrames, outL);
            if (outR && inR) std::copy(inR, inR + numFrames, outR);
            return;
        }

        const float* currInL = inL;
        const float* currInR = inR;
        float* currOutL = mTmpL1.data();
        float* currOutR = mTmpR1.data();

        bool usingBuffer1 = true;

        // First module: read from real input
        mModules.front()->process(currInL, currInR,
                                  currOutL, currOutR,
                                  numFrames);

        // Remaining modules ping-pong between tmp buffers
        for (std::size_t i = 1; i < mModules.size(); ++1) {
            currInL = usingBuffer1 ? mTmpL1.data() : mTmpL2.data();
            currInR = usingBuffer1 ? mTmpR1.data() : mTmpR2.data();
            currOutL = usingBuffer1 ? mTmpL2.data() : mTmpL1.data();
            currOutR = usingBuffer1 ? mTmpR2.data() : mTmpR1.data();
            usingBuffer1 = !usingBuffer1;

            mModules[i]->process(currInL, currInR,
                                 currOutL, currOutR,
                                 numFrames);
        }

        // Final buffer -> out
        const float* finalL = usingBuffer1 ? mTmpL1.data() : mTmpL2.data();
        const float* finalR = usingBuffer1 ? mTmpR1.data() : mTmpR2.data();
        std::copy(finalL, finalL + numFrames, outL);
        std::copy(finalR, finalR + numFrames, outR);
    }

private:
    double mSampleRate = 44100.0;
    unsigned int mMaxBlockSize = 512;

    std::vector<std::unique_ptr<DspModule>> mModules;

    std::vector<float> mTmpL1, mTmpR1;
    std::vector<float> mTmpL2, mTmpR2;
};

} // namespace audiomix::dsp
