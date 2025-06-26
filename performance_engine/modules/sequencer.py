import time
import threading
from performance_engine.modules.sampler import trigger_sample
from audioscript_runtime import say, pulse

patterns = {}

def define_pattern(name, sample, pattern_str):
    # Example pattern_str: "1,0,0,1,0,1"
    steps = [int(x.strip()) for x in pattern_str.split(",")]
    patterns[name] = {
        "sample": sample,
        "steps": steps
    }
    say(f"🎼 Pattern defined: {name} → {sample} | Steps: {steps}")

def play_pattern(name, bpm=120):
    bpm = float(bpm)
    if name not in patterns:
        say(f"❌ Pattern not found: {name}", "🚫")
        return

    data = patterns[name]
    sample = data["sample"]
    steps = data["steps"]
    interval = 60.0 / bpm # seconds per beat

    def sequence_loop():
        say(f"▶️ Playing pattern: {name} @ {bpm} BPM", "🎚️")
        for i, step in enumerate(steps):
            if step:
                trigger_sample(sample)
                pulse("cyan", bpm)
            time.sleep(interval)
        say(f"▶️ Pattern finished: {name}", "✅")

    threading.Thread(target=sequence_loop).start()

def register():
    return {
        "define_pattern": define_pattern,
        "play_pattern": play_pattern
    }
