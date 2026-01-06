// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/gain_module.cpp

// Refer to gain_module.h

#include "audio/dsp/modules/gain_module.h"

#include <algorithm>

namespace audiomix::dsp {

void GainModule::prepare(double sampleRate, unsigned int maxBlockSize) {
    mSampleRate = sampleRate;
    mMaxBlockSize = maxBlockSize;

    // initialize to unity
    mGainDb = 0.0f;
    mGainLin.setTarget(dbToLinear(mGainDb));
    mGainLin.prepare(mSampleRate, mSmoothingMs);
}

void GainModule::reset() {
    // reset smoother back to current gain
    mGainLin.setTarget(dbToLinear(mGainDb));
    mGainLin.prepare(mSampleRate, mSmoothingMs);
}

void GainModule::setSmoothingTimeMs(float ms) {
    mSmoothingMs = ms;
    mGainLin.setTimeMs(ms);
}

void GainModule::setGainDb(float db) {
    mGainDb = db;

    // convert once (smoothing happens linearly)
    const float targetLin = dbToLinear(mGainDb);
    mGainLin.setTarget(targetLin);
}

void GainModule::setParameter(const std::string& id, float value) {
    // string IDs kept here (AS-friendly)
    // function called from a control thread, not audio callback
    if (id == "gain_db" || id == "gain" || id == "volume_db") {
        setGainDb(value);
    } else if (id == "smoothing_ms") {
        setSmoothingTimeMs(value);
    }
}

void GainModule::process(const float* inL, const float* inR,
                         float* outL, float* outR,
                         unsigned int numFrames)
{
    if (numFrames == 0) return;

    // null-safe behavior
    // if outputs are null, nothing to write
    if (!outL && !outR) return;

    // if inputs are null, treat as silence
    // upstream chain feeds zero for missing inputs
    // this function keeps module robust
    if (!inL && outL) std::fill(outL, outL + numFrames, 0.0f);
    if (!inR && outR) std::fill(outR, outR + numFrames, 0.0f);

    // apple smoothed linear gain sample-by-sample
    // cheap (less tech debt/scalable), avoids zipper noise on fader moves
    for (unsigned int i = 0; i < numFrames; ++i) {
        const float g = mGainLin.process();

        if (inL && outL) outL[i] = inL[i] * g;
        if (inR && outR) outR[i] = inR[i] * g;
    }
}

} // namespace audiomix::dsp
