// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/compressor_module.h
//
/*
  Single-band feed-forward compressor with branching peak detector.
  
  Designed for:
    - Stereo or N-channel processing via processMulti()
    - Linked or dual-mono detection
    - Optional sidechain input (external buffer routed through processMulti())
    - Optional highpass (hp) on the detection path (RBJ, computed off audio threshold)
    - Soft knee w/ quadratic interpolation around threshold
    - Wet/dry blend (parallel compression in-module)
    - Externally readable gain reduction in dB (atomic, lock-free)
    
    Threading model:
      - Control thread builds CompPacket in setParams() and publishes via atomic index (same double-buffered pattern as EqModule)
      - Audio thread consumes the latest packet at processMulti() boundary, updates smoothing targets, then runs sample by sample
      
    TODO: Detector mode is currently Branching only.
    Decoupled and Rms are reserved in CompressorParams and will fall back to Branching/Peak until implemented.
*/

#pragma once
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include <cstddef>
#include <atomic>

#include "../core/dsp_module.h"
#include "../core/biquad.h"
#include "../core/rbj_coeffs.h"
#include "../core/compressor_params.h"
#include "eq_module.h"

namespace audiomix::dsp {

  class CompressorModule final : public DspModule {
  public:
    CompressorModule() = default;
    
    // Stereo wrapper - delegates to processMulti() with no sidechain
    void process(const float* inL, const float* inR, float* outL, float* outR, unsigned int numFrames) override {
      const float* inputs[2] = { inL, inR };
      float* outputs[2] = { outL, outR };
      processMulti(inputs, outputs, 2, numFrames);
    }

    void prepare(double sr, unsigned int maxBlock) override {
      mSampleRate = (sr > 0.0) ? sr : 44100.0;
      mMaxBlock = (maxBlock > 0) ? maxBlock : 512;
      
      mPacketReadyIndex.store(-1, std::memory_order_relaxed);
      mPacketWriteIndex.store(0, std::memory_order_relaxed);
      mPrepared = true;
    }

    void reset() override {
      for (auto& env : mEnvelope) env = 0.0f;
      for (auto& sc : mSidechainState) sc = {};

      mGainReductionDb.store(0.0f, std::memory_order_relaxed);

      mAttackCoeff = 0.0f;
      mReleaseCoeff = 0.0f;
      mScHpCurrent = rbj::identity();
      mScHpTarget = rbj::identity();
      mScHpTarget = {};
      mScHpSmoothRemaining = 0;

      mActive = CompressorParams{};
      mPacketReadyIndex.store(-1, std::memory_order_relaxed);
    }

    // Control thread API
    // build coeff packet, publishes atomically
    void setParams(const CompressorParams& p, float smoothMs = 10.0f) {
      CompressorParams params = p;
      sanitize(params);

      const double sr = (params.sample_rate > 0) ? static_cast<double>(params.sample_rate) : mSampleRate;

      CompPacket pkt{};
      pkt.active = params;
      pkt.sampleRate = sr;
      pkt.smoothSamples = std::max(1, static_cast<int>(smoothMs * 0.001f * static_cast<float>(sr)));

      // Envelope coeffs - exponential one-pole smoothing
      // coeff = exp(-1 / (timeMs * 0.001 * sr))
      pkt.attackCoeff = computeEnvCoeff(params.attack_ms, sr);
      pkt.releaseCoeff = computeEnvCoeff(params.release_ms, sr);

      // Threshold/ratio/knee in working unit
      pkt.thresholdDb = params.threshold_db;
      pkt.ratio = params.ratio;
      pkt.kneeDb = params.knee_db;
      pkt.makeupDb = db_to_lin(params.makeup_db);
      pkt.mix = params.mix;

      // Sidechain HP coeffs
      // Re-ealuated p/packet since sr may change since prepare()
      pkt.scHpEnabled = params.sidechain_hp_enabled;
      pkt.scHpTarget = params.sidechain_hp_enabled ? rbj::highpass(params.sidechain_hp_hz, params.sidechain_hp_q, sr) : rbj::identity();

      publishPacket(pkt);
    }
    
    // Audio thread N-channel processing with optional sidechain
    // sidechain: optional pointer to an array of channel pointers
    // if params.sidechain_external is true and non-null, detection uses sidechain buffer
    // otherwise, detection uses main input buffer (first 2 channels if stereo)
    void processMulti(const float* const* inputs, float* const* outputs, unsigned int numChannels, unsigned int numFrames) override {
      if (!mPrepared || numChannels == 0 || numFrames == 0) return;

      consumePendingPacket();
      ensureChannels(numChannels);

      const unsigned int frames = std::min(numFrames, mMaxBlock);
      const bool linked = (mActive.stereo_link == StereoLink::Linked);
      const bool useScHp = mActive.sidechain_hp_enabled

      // external sidechain plumbing reserved
      // currently always uses main input for detection
      // TODO: when chain wires sidechain routing, this where the input pointer will swtich.
      const float* const* detectionSource = inputs;

      for (unsigned int i = 0; i < frames; ++i) {
        // smooth sidechain HP coeffs toward target if enabled
        if (useScHp && mScHpSmoothRemaining > 0) {
          mScHpCurrent.b0 += mScHpDelta.b0;
          mScHpCurrent.b1 += mScHpDelta.b1;
          mScHpCurrent.b2 += mScHpDelta.b2;
          mScHpCurrent.a1 += mScHpDelta.a1;
          mScHpCurrent.a2 += mScHpDelta.a2;
          --mScHpSmoothRemaining;
        }

        // build detection signal
        // linked: max abs across channels
        float detectionSample = 0.0f;

        if (linked) {
          // linked: take max absolute value across all channels for detection
          for (unsigned int ch = 0; ch < numChannels; ++ch) {
            const float* dIn = (detectionSource && detectionSource[ch]) ? detectionSource[ch] : nullptr;
            const float s = dIn ? dIn[i] : 0.0f;
            const float filtered = useScHp ? biquad_process_sample(mScHpCurrent, s, &mSidechainState[ch]) : s;
            const float a = std::fabs(filtered);
            if (a > detectionSample) detectionSample = a;
          }
        }

        // compute gain reduction (single value if linked)
        float linkedGainLin = 1.0f;
        float linkedGrDb = 0.0f;

        if (linked) {
          updateEnvelope(mEnvelope[0], detectionSample);
          const float grDb = computeGainReduction(mEnvelope[0]);
          linkedGrDb = grDb;
          linkedGainLin = db_to_lin(-grDb);
        }

        // apply per channel gain reduction with linked detection if linked, or independent detection if dual-mono
        float maxGrDbThisSample = linkedGrDb;

        for (unsigned int ch = 0; ch < numChannels; ++ch) {
          const float* in = (inputs && inputs[ch]) ? inputs[ch] : nullptr;
          float* out = (outputs && outputs[ch]) ? outputs[ch] : nullptr;
          if (!out) continue;

          const float dry = in ? in[i] : 0.0f;
          float gainLin = linkedGainLin;

          if (linked) {
            // dual-mono: compute per-channel gain reduction, but still use linked detection/envelope
            const float* dIn = (detectionSource && detectionSource[ch]) ? detectionSource[ch] : nullptr;
            const float s = dIn ? dIn[i] : 0.0f;
            const float filtered = useScHp ? biquad_process_sample(mScHpCurrent, mSideChainState[ch], s) : s;
            const float det = std::fabs(filtered);

            updateEnvelope(mEnvelope[ch], det);
            const float grDb = computeGainReduction(mEnvelope[ch]);
            if (grDb > maxGrDbThisSample) maxGrDbThisSample = grDb;
            gainLin = db_to_lin(-grDb);
          }

          const float wet = dry * gainLin * mActive_makeupLin;
          out[i] = (1.0f - mActive.mix) * dry + mActive.mix * wet;
        }

        // publish gain reduction readout (last sample of block wins)
        if (i + 1 == frames) {
          mGainReductionDb.store(maxGrDbThisSample, std::memory_order_relaxed);
        }
      } 
    }

    // Public readout - gain reduction in dB (postive = compressing)
    // Lock-free, safe to read from any thread
    // e.g., LEDs, modulation, UI, etc.
    float getGainReductionDb() const {
      return mGainReductionDb.load(std::memory_order_relaxed);
    }
  
  private:
    // Helpers
    static inline float clampf(float v, float lo, float hi) {
      return std::max(lo, std::min(hi, v));
    }

    static inline float db_to_lin(float db) {
      return std::pow(10.0f, db * 0.05f);
    }

    static inline float lin_to_db(float lin) {
      // floor to avoid log(0); -120 dB is well below audible
      // threshold and effectively silence for gain reduction readout purposes
      return 20.0f * std::log10(std::max(lin, 1.0e-6f));
    }

    static float computeEnvCoeff(float timeMs, double sampleRate) {
      const float timeSec = std::max(0.001f, timeMs * 0.001f);
      return std::exp(-1.0f / (timeSec * static_cast<float>(sampleRate)));
    }
  };

} // namespace audiomix::dsp