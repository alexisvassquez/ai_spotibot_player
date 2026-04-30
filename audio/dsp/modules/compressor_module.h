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

    }  
  };
}