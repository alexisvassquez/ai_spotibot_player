# ai_spotibot_player
# AudioMIX
# performance_engine/modules/context.py

"""
Central runtime context for AudioMIX

This module owns:
- command registry
- session state
- event bus

All runtime modules import shared state from here.
"""

# Command Registry
command_registry = {}

# Runtime State
from performance_engine.session_state import SessionState
from performance_engine.event_bus import EventBus

session = SessionState()
events = EventBus()
