# ai_spotibot_player
# AudioMIX
# audio/ai/schemas.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

"""
Shared data contracts for AudioMIX AI modules.
These dataclasses give the AI pipeline a consistent vocab so that:
  1. extractors return structured feats
  2. inference returns structured predictions
  3. planners/runtime consume structured recommendations
"""

# structured audio feats extracted from a source track
# will be adjusted over time to match real outputs
@dataclass
class AudioFeatures:
    source_path: str
    bpm: Optional[float] = None
    duration: Optional[float] = None
    sample_rate: Optional[int] = None

    rms: Optional[float] = None
    zero_crossing_rate: Optional[float] = None
    centroid_mean: Optional[float] = None
    rolloff_mean: Optional[float] = None

    mfcc_mean: List[float] = field(default_factory=list)
    spectral_contrast_mean: List[float] = field(default_factory=list)

    raw_features: Dict[str, Any] = field(default_factor=dict)

# output from predict_eq / inference_engine
@dataclass:
class EQPrediction:
    labels: List[str] = field(default_factory=list)
    confidences: Dict[str, float] = field(default_factory=dict)
    model_name: Optional[str] = None
    notes: Optional[str] = None

# output from mood_classifier
@dataclass
class MoodPrediction:
    label: str = "unknown"    # e.g., mellow, hyper, angry, energetic, ambient
    confidence: float = 0.0
    scores: Dict[str, float] = field(default_factory=dict)
    model_name: Optional[str] = None

# output from audience_listener - live energy sensing
@dataclass
class AudienceState:
    energy_level: str = "unknown"    # e.g., calm, rising, hype, overload
    loudness: Optional[float] = None
    confidence: float = 0.0
    notes: Optional[str] = None

# generic performance recommendation for lighting behavior
# does not assume LED hardware (yet)
# TODO: hook into HAL (hardware abstraction layer)
# lighting, visuals, FX, automation, or stage control
@dataclass
class PerformanceSuggestion:
    mood: str
    intensity: float
    bpm: Optional[float] = None
    color_hint: Optional[str] = None
    effect_hint: Optional[str] = None
    eq_hint: Optional[str] = None
    reason: str = ""

# IR compiled AudioScript emitted by AI decision layer
@dataclass
class AudioScriptSuggestion:
    script: str
    summary: str

# final combined recommendation produced by the decision_engine
@dataclass
class AIRecommendation:
    audio_features: Optional[AudioFeatures] = None
    eq_prediction: Optional[EQPrediction] = None
    mood_prediction: Optional[MoodPrediction] = None
    audience_state: Optional[AudienceState] = None
    performance_suggestion: Optional[PerformanceSuggestion] = None
    audioscript_suggestion: Optional[AudioScriptSuggestion] = None

    overall_confidence: float = 0.0
    confidence_tier: str = "low"
    notes: List[str] = field(default_factory=list)
