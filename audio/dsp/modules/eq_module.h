// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/eq_module.h

// RBJ Cookbook coefficient builders
//   - peaking, lowshelf, highshelf
// Calculates digital biquad filter coeffs (a, b) used in EQ
// Handles N channels (multichannel signals) - however many DspChain provides
// Introduces EQ coeff packet - moves coefficient generation off audio thread

#pragma once
#include <vector>
#include <array>
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <atomic>
#include <mutex>

#include "audio/dsp/core/dsp_module.h"
#include "audio/dsp/core/biquad.h"
#include "audio/dsp/core/eq_params.h"

namespace audiomix::dsp {

// a0 normalized to 1
class EqModule final : public DspModule {
public:
    EqModule() = default;

    // thin stereo wrapper around processMulti()
    void process(const float* inL, const float* inR,
                 float* outL, float* outR,
                 unsigned int numFrames) override {
        const float* const inputs[2] = { inL, inR };
        float* const outputs[2] = { outL, outR };
        processMulti(inputs, outputs, 2, numFrames);
    }

    void prepare(double sr, unsigned int maxBlock) override {
        mSampleRate = (sr > 0.0) ? sr : 44100.0;          // 44.1 kHz
        mMaxBlock   = (maxBlock > 0) ? maxBlock : 512;    // 512 buffer size

        // Default: chain is 4ch (Master L/R + Booth L/R)
        // allocate per actual processMulti channel count lazily
        // Coeffs are fixed-size (10 band EQ), states allocated for channels
        // Starts in a known state (no pending packets)
        mPacketReadyIndex.store(-1, std::memory_order_relaxed);
        mPacketWriteIndex.store(0, std::memory_order_relaxed);
        mPrepared = true;
    }

    void reset() override {
        std::fill(mPreampLin.begin(), mPreampLin.end(), 1.0f);
        for (auto& stCh : mState) {
            for (auto& stBand : stCh) stBand = {};
        }
        for (int b = 0; b < EqParams::kMaxBands; ++b) {
            mCurrent[b] = identity();
            mTarget[b] = identity();
            mDelta[b] = {};
            mSmoothRemaining[b] = 0;
        }
        mPreampTarget = 1.0f;
        mPreampDelta = 0.0f;
        mPreampSmoothRemaining = 0;
        mActive = EqParams{};
        mPacketReadyIndex.store(-1, std::memory_order_relaxed);
    }

    // Control thread API
    // Builds target coeffs off audio thread
    // publishes immutable packet that the audio thread can consume lock-free
    void setParams(const EqParams& p, float smoothMs = 10.0f) {
        EqParams params = p;
        sanitize(params);

        // compute coeffs are normalized
        CoeffPacket pkt{};
        pkt.active = params;

        const double sr = (params.sample_rate > 0) ? params.sample_rate : mSampleRate;
        pkt.sampleRate = sr;

        pkt.smoothSamples = std::max(1, static_cast<int>(smoothMs * 0.001f * static_cast<float>(sr)));

        pkt.preampTarget = db_to_lin(params.preamp_db);

        const int n = std::min(params.band_count, EqParams::kMaxBands);
        pkt.bandCount = n;

        for (int i = 0; i < EqParams::kMaxBands; ++i) {
            pkt.targets[i] = (i < n && params.bands[i].enabled)
                ? makeBand(params.bands[i], sr)
                : identity();
        }

        publishPacket(pkt);
    }

    void processMulti(const float* const* input,
                      float* const* outputs,
                      unsigned int numChannels,
                      unsigned int numFrames) override
    {
        if (!mPrepared || numChannels == 0 || numFrames == 0) return;

        // consume control thread updates
        consumePendingPacket();

        // ensure channel state exists
        // one time allocation if channel count changes
        ensureChannels(numChannels);

        const unsigned int frames = std::min(numFrames, mMaxBlock);
        const int bandCount = std::min(mActive.band_count, EqParams::kMaxBands);

        for (unsigned int ch = 0; ch < numChannels; ++ch) {
            const float* in = input && input[ch] ? input[ch] : nullptr;
            float* out = outputs ? outputs[ch] : nullptr;
            if (!out) continue;

            // if input missing, treat as silence
            for (unsigned int i = 0; i < frames; ++i) {
                if (mPreampSmoothRemaining > 0) {
                    mPreampLinGlobal += mPreampDelta;
                    --mPreampSmoothRemaining;
                }
                float x = (in ? in[i] : 0.0f) * mPreampLinGlobal;

                for (int b = 0; b < bandCount; ++b) {
                    if (mSmoothRemaining[b] > 0) {
                        mCurrent[b].b0 += mDelta[b].b0;
                        mCurrent[b].b1 += mDelta[b].b1;
                        mCurrent[b].b2 += mDelta[b].b2;
                        mCurrent[b].a1 += mDelta[b].a1;
                        mCurrent[b].a2 += mDelta[b].a2;
                        --mSmoothRemaining[b];
                    }
                    x = biquad_process_sample(mCurrent[b], mState[ch][b], x);
                }

                out[i] = x;
            }
        }
    }

private:
    static inline float clampf(float v, float lo, float hi) {
        return std::max(lo, std::min(v, hi));
    }

    static BiquadCoeffs identity() {
        return BiquadCoeffs{1, 0, 0, 0, 0};
    }

    static void sanitize(EqParams& p) {
        p.sample_rate = (p.sample_rate > 0) ? p.sample_rate : 44100;    // 44.1 kHz
        p.preamp_db = clampf(p.preamp_db, -24.0f, 24.0f);
        p.band_count = std::max(0, std::min(p.band_count, EqParams::kMaxBands));

        for (int i = 0; i < p.band_count; ++i) {
            p.bands[i].f0 = clampf(p.bands[i].f0, 20.0f, 20000.0f);    // 20k Hz
            p.bands[i].q = clampf(p.bands[i].q, 0.1f, 18.0f);    // q factor (narrow/wide)
            p.bands[i].gain_db = clampf(p.bands[i].gain_db, -24.0f, 24.0f); // gain limit
        }
    }

    void ensureChannels(unsigned int numChannels) {
        if (mState.size() == numChannels) return;

        mState.assign(numChannels, {});
        mPreampLin.assign(numChannels, 1.0f);

        // each channel has 10 band states
        for (auto& stCh : mState) {
            stCh.fill({});
        }
    }

    // RBJ cookbook: normalized a0=1
    BiquadCoeffs makeBand(const EqBand& band, double sampleRate) const {
        const float f0 = clampf(band.f0, 20.0f, 20000.0f);
        const float q = clampf(band.q, 0.1f, 18.0f);
        const float gainDb = clampf(band.gain_db, -24.0f, 24.0f);

        // w0 = normalized cutoff freq
        const float w0 = 2.0f * static_cast<float>(M_PI) * (f0 / static_cast<float>(sampleRate));
        const float cosw0 = std::cos(w0);
        const float sinw0 = std::sin(w0);

        const float A = std::pow(10.0f, gainDb / 40.0f);

        if (band.type == EqBandType::Peaking) {
            const float alpha = sinw0 / (2.0f * q);

            const float b0 = 1.0f + alpha * A;
            const float b1 = -2.0f * cosw0;
            const float b2 = 1.0f - alpha * A;
            const float a0 = 1.0f + alpha / A;
            const float a1 = -2.0f * cosw0;
            const float a2 = 1.0f - alpha / A;

            return normalize(b0, b1, b2, a0, a1, a2);
        }

        // Shelves: slope S=1
        const float S = 1.0f;
        const float alpha = sinw0 / 2.0f * std::sqrt((A + 1.0f/A) * (1.0f/S - 1.0f) + 2.0f);
        const float sqrtA = std::sqrt(A);

        if (band.type == EqBandType::LowShelf) {
            const float b0 =    A*((A+1) - (A-1)*cosw0 + 2*sqrtA*alpha);
            const float b1 =  2*A*((A-1) - (A+1)*cosw0);
            const float b2 =    A*((A+1) - (A-1)*cosw0 - 2*sqrtA*alpha);
            const float a0 =        (A+1) + (A-1)*cosw0 + 2*sqrtA*alpha;
            const float a1 =    -2*((A-1) + (A+1)*cosw0);
            const float a2 =        (A+1) + (A-1)*cosw0 - 2*sqrtA*alpha;

            return normalize(b0, b1, b2, a0, a1, a2);
        }

        // HighShelf
        {
            const float b0 =    A*((A+1) + (A-1)*cosw0 + 2*sqrtA*alpha);
            const float b1 = -2*A*((A-1) + (A+1)*cosw0);
            const float b2 =    A*((A+1) + (A-1)*cosw0 - 2*sqrtA*alpha);
            const float a0 =        (A+1) - (A-1)*cosw0 + 2*sqrtA*alpha;
            const float a1 =    2*((A-1) - (A+1)*cosw0);
            const float a2 =        (A+1) - (A-1)*cosw0 - 2*sqrtA*alpha;

            return normalize(b0, b1, b2, a0, a1, a2);
        }
    }

    static BiquadCoeffs normalize(float b0, float b1, float b2, float a0, float a1, float a2) {
        BiquadCoeffs c;
        const float invA0 = 1.0f / a0;
        c.b0 = b0 * invA0;
        c.b1 = b1 * invA0;
        c.b2 = b2 * invA0;
        c.a1 = a1 * invA0;
        c.a2 = a2 * invA0;
        return c;
    }

private:
    struct CoeffPacket {
        EqParams active{};
        double sampleRate = 44100.0;    // 44.1 kHz

        int bandCount = 0;
        int smoothSamples = 1;

        float preampTarget = 1.0f;
        std::array<BiquadCoeffs, EqParams::kMaxBands> targets{};
    };

    // control thread publishes fully-computed packet into dbl buffer
    // audio thread consumes packet w/o locks via an atomic index
    void publishPacket(const CoeffPacket& pkt) {
        const int next = 1 - mPacketWriteIndex.load(std::memory_order_relaxed);
        mPackets[next] = pkt;
        mPacketWriteIndex.store(next, std::memory_order_relaxed);
        mPacketReadyIndex.store(next, std::memory_order_release);
    }

    void consumePendingPacket() {
        const int idx = mPacketReadyIndex.exchange(-1, std::memory_order_acq_rel);
        if (idx < 0) return;

        const CoeffPacket& pkt = mPackets[idx];

        // update runtime state atomically at boundary (1x p/pkt)
        mActive = pkt.active;
        mSampleRate = (pkt.sampleRate > 0.0) ? pkt.sampleRate : mSampleRate;

        const int smoothSamples = std::max(1, pkt.smoothSamples);

        // preamp smoothing targets (deltas)
        // audio thread only writes smoothing state
        mPreampTarget = pkt.preampTarget;
        mPreampSmoothRemaining = smoothSamples;
        mPreampDelta = (mPreampTarget - mPreampLinGlobal) / static_cast<float>(smoothSamples);

        // band smoothing
        // audio thread only writes smoothing state
        for (int i = 0; i < EqParams::kMaxBands; ++i) {
            mTarget[i] = pkt.targets[i];

            mSmoothRemaining[i] = smoothSamples;
            mDelta[i].b0 = (mTarget[i].b0 - mCurrent[i].b0) / smoothSamples;
            mDelta[i].b1 = (mTarget[i].b1 - mCurrent[i].b1) / smoothSamples;
            mDelta[i].b2 = (mTarget[i].b2 - mCurrent[i].b2) / smoothSamples;
            mDelta[i].a1 = (mTarget[i].a1 - mCurrent[i].a1) / smoothSamples;
            mDelta[i].a2 = (mTarget[i].a2 - mCurrent[i].a2) / smoothSamples;
        }
    }

private:
    double mSampleRate = 44100.0;    // 44.1 kHz
    unsigned int mMaxBlock = 512;    // max buffer size 512 samples
    bool mPrepared = false;

    // dbl-buffered param pkts (control -> audio)
    std::array<CoeffPacket, 2> mPackets{};
    std::atomic<int> mPacketReadyIndex{-1};
    std::atomic<int> mPacketWriteIndex{0};

    EqParams mActive{};

    // Coeff smoothing
    // shared across channels, states are p/channel
    std::array<BiquadCoeffs, EqParams::kMaxBands> mCurrent{};
    std::array<BiquadCoeffs, EqParams::kMaxBands> mTarget{};
    std::array<BiquadCoeffs, EqParams::kMaxBands> mDelta{};
    std::array<int, EqParams::kMaxBands> mSmoothRemaining{};

    // p/channel, p/band states
    std::vector<std::array<BiquadState, EqParams::kMaxBands>> mState;

    // Preamp smoothing
    float mPreampLinGlobal = 1.0f;
    float mPreampTarget = 1.0f;
    float mPreampDelta = 0.0f;
    int mPreampSmoothRemaining = 0;

    // p/channel preamp cache
    // reserved
    std::vector<float> mPreampLin;
};

} // namespace audiomix::dsp
