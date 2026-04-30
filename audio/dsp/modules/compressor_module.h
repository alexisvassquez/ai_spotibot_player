// ai_spotibot_player
// AudioMIX
// audio/dsp/modules/compressor_module.h

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

namespace audiomix::dsp {}