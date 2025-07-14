import os
import subprocess
from performance_engine.modules.track_engine import track_registry
from performance_engine.modules.led_controller import pulse
from performance_engine.utils.shell_output import say

sample_registry = {}

def load_sample(name, path):
    if not os.path.exists(path):
        say(f"❌ File not found: {path}", "⚠️")
        return
    sample_registry[name] = path
    say(f"Sample loaded: {name} → {path}", "📂")

def trigger_sample(name):
    path = sample_registry.get(name)
    if not path:
        say(f"❌ Sample not found: {name}", "🚫")
        return

    say(f"💥 Triggering sample: {name}", "🎧")
    subprocess.Popen(["aplay", path])

    # Pulse LED for feedback
    pulse("yellow", 140)

def register():
    return {
        "load_sample": load_sample,
        "trigger_sample": trigger_sample
    }
