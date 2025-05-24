from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry

def list_commands(*args):
    say("Available AudioScript Commands:", "🃏")
    if not command_registry:
        say("⚠️ Registry is empty!")
    else:
        for cmd in sorted(command_registry.keys()):
            say(f" - {cmd}")

def register():
    return {
        "list_commands": list_commands
    }
