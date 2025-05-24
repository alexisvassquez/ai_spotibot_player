from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry

def play(track):
    say(f"Now playing: {track}", "🔊")

def register():
    return {
        "play": play,
    }
