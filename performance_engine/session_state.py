# ai_spotibot_player
# AudioMIX
# performance_engine/session_state.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SessionState:
    # Transport
    is_playing: bool = False
    current_track: Optional[str] = None
    playback_position: float = 0.0    # seconds

    # Musical context
    bpm: Optional[int] = None
    key: Optional[str] = None
    mood: str = "neutral"

    # Mix context
    eq_profile: Optional[str] = None
    gain: float = 1.0
    pan: int = 0    # -100 (L) -> 0 (center) -> +100 (R)

    # Lighting
    active_zones: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Debug/introspection
    last_event: Optional[str] = None
