// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/clipper_module.cpp
//
// Safe with multichannel bridge

#include "clipper_module.h"

namespace audiomix::dsp {

void ClipperModule::prepare(double sampleRate, unsigned int maxBlockSize) {
    mSampleRate = (sampleRate > 1.0) ? sampleRate : 44100.0;    // 44.1 kHz
    mMaxBlockSize = maxBlockSize;

    // prep smoothers w/ current smoothing time
    mDriveLin.prepare(mSampleRate, mSmoothingMs);
    mCeilingLin.prepare(mSampleRate, mSmoothingMs);
    mMixSmoothed.prepare(mSampleRate, std::max(5.0f, mSmoothingMs * 0.5f));

    // set initial targets based on current UI-domain state
    mDriveLin.setTarget(dBToLinear(mDriveDb));
    mCeilingLin.setTarget(dBToLinear(mCeilingDb));
    mMixSmoothed.setTarget(clampf(mMix, 0.0f, 1.0f));

    // force current toward target immediately by doing one process step if needed
    // SmoothedParameter snaps current to target when ms<=0
    (void)mDriveLin.process();
    (void)mCeilingLin.process();
    (void)mMixSmoothed.process();
}

void ClipperModule::reset() {
    // "Reset" means clear state
    // for stateless module, we re-init smoothing
    // prepare() aligns current to target - reset() maintains consistency
    mDriveLin.prepare(mSampleRate, mSmoothingMs);
    mCeilingLin.prepare(mSampleRate, mSmoothingMs);
    mMixSmoothed.prepare(mSampleRate, std::max(5.0f, mSmoothingMs * 0.5f));

    mDriveLin.setTarget(dBToLinear(mDriveDb));
    mCeilingLin.setTarget(dBToLinear(mCeilingDb));
    mMixSmoothed.setTarget(clampf(mMix, 0.0f, 1.0f));
}

void ClipperModule::setSmoothingTimeMs(float ms) {
    mSmoothingMs = clampf(ms, 0.0f, 200.0f);

    // SmoothedParameter snaps if ms==0
    mDriveLin.setTimeMs(mSmoothingMs);
    mCeilingLin.setTimeMs(mSmoothingMs);
    mMixSmoothed.setTimeMs(std::max(5.0f, mSmoothingMs * 0.5f));
}

void ClipperModule::setDriveDb(float db) {
    mDriveDb = clampf(db, -60.0f, 24.0f);
    mDriveLin.setTarget(dBToLinear(mDriveDb));
}

void ClipperModule::setCeilingDb(float db) {
    // ceiling should not exceed 0 dBFS
    mCeilingDb = clampf(db, -60.0f, 0.0f);
    mCeilingLin.setTarget(dBToLinear(mCeilingDb));
}

void ClipperModule::setMix(float mix01) {
    mMix = clampf(mix01, 0.0f, 1.0f);
    mMixSmoothed.setTarget(mMix);
}

void ClipperModule::setParameter(const std::string& id, float value) {
    if (id == "drive.db" || id == "drive_db" || id == "drive") {
        setDriveDb(value);
    } else if (id == "ceiling.db" || id == "ceiling_db" || id == "ceiling") {
        setCeilingDb(value);
    } else if (id == "mix" || id == "wet") {
        setMix(value);
    } else if (id == "mode") {
        mMode = (value < 0.5f) ? Mode::Hard : Mode::Soft;
    }
}

void ClipperModule::process(const float* inL, const float* inR,
                            float* outL, float* outR,
                            unsigned int numFrames) {
    if (numFrames == 0) return;

    // processMulti bridge can invoke process w/ a missing output (defensive)
    const bool hasOutL = (outL != nullptr);
    const bool hasOutR = (outR != nullptr);
    if (!hasOutL && !hasOutR) return;

    // process per-sample to get smooth parameter changes w/o stepping artifacts
    // cheap (light tech debt - few mulitplies + tanh/clamp)
    for (unsigned int i = 0; i < numFrames; ++i) {
        const float dryL = (inL ? inL[i] : 0.0f);
        const float dryR = (inR ? inR[i] : 0.0f);

        const float drive   = mDriveLin.process();
        const float ceiling = mCeilingLin.process();
        const float mix     = mMixSmoothed.process();

        const float xL = dryL * drive;
        const float xR = dryR * drive;

        float wetL = 0.0f;
        float wetR = 0.0f;

        if (mMode == Mode::Hard) {
            wetL = hardClip(xL, ceiling);
            wetR = hardClip(xR, ceiling);
        } else {
            wetL = softClipTanh(xL, ceiling);
            wetR = softClipTanh(xR, ceiling);
        }

        const float yL = dryL + (wetL - dryL) * mix;
        const float yR = dryR + (wetR - dryR) * mix;

        if (hasOutL) outL[i] = yL;
        if (hasOutR) outR[i] = yR;
    }
}

// Placeholders
// reflects GainModule
void ClipperModule::registerParameters(control::ParamRegistry& /*registry*/) {}
void ClipperModule::bindParameters(control::ParamBindingTable& /*bindings*/) {}

} // namespace audiomix::dsp


