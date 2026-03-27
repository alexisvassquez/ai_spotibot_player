# ai_spotibot_player
# AudioMIX
# audio/ai/core/confidence.py

from __future__ import annotations
from typing import Dict, Iterable, Optional

"""
Confidence utilities for AudioMIX AI predictions.
Keeps threshold logic centralized so every module is not
acting on its own
"""

HIGH_CONFIDENCE = 0.80
MEDIUM_CONFIDENCE = 0.55

# normalize score into [0.0, 1.0]
def clamp_confidence(score: Optional[float]) -> float:
    if score is None:
        return 0.0
    return max(0.0, min(1.0, float(score)))

# map numeric confidence to a named tier
def confidence_tier(score: Optional[float]) -> str:
    value = clamp_confidence(score)
    if value >= HIGH_CONFIDENCE:
        return "high"
    if value >= MEDIUM_CONFIDENCE:
        return "medium"
    return "low"

# True when a prediction is strong enough for auto/assertive recommendation
def should_apply(score: Optional[float], threshold: float = HIGH_CONFIDENCE) -> bool:
    return clamp_confidence(score) >= threshold

# simple average of valid confidences
# keeps behavior understandable + easy to debug
def combine_confidences(scores: Iterable[Optional[float]]) -> float:
    values = [clamp_confidence(score) for score in scores if score is not None]
    if not values:
        return 0.0
    return sum(values) / len(values)

# return the strongest class confidence from a label->score mapping
def top_confidence(confidences: Dict[str, float]) -> float:
    if not confidences:
        return 0.0
    return clamp_confidence(max(confidences.values()))

# return label w/ the highest confidence
def pick_best_label(confidences: Dict[str, float]) -> Optional[str]:
    if not confidences:
        return None
    return max(confidences, key=confidences.get)
