# ai_spotibot_player
# AudioMIX
# performance_engine/event_bus.py

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def on(self, event_name, handler):
        self._subscribers.setdefault(event_name, []).append(handler)

    def emit(self, event_name, payload=None):
        for handler in self._subscribers.get(event_name, []):
            handler(payload)
