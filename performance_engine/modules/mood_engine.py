from performance_engine.utils.shell_output import say
from performance_engine.modules.context import command_registry

def mood_set(mood):
    say(f"[MOOD] context set to: {mood}", "🎼")

def register():
    return {
        "mood.set": mood_set,
    }
