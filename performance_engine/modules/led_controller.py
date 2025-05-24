import sys
sys.path.append("audio/led")

from audio.led.controller import LightController
from audio_reactive import react_to_audio
from color_profiles import get_color_for_mood
from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry

led = LightController()

def glow(color_name):
    rgb = get_color_for_mood(color_name)
    led.set_color(rgb)
    say(f"LED glowing {color_name}", "💡")

def pulse(color_name, bpm):
    rgb = get_color_for_mood(color_name)
    led.pulse(rgb, int(bpm))
    say(f"Pulsing {color_name} @ {bpm} BPM", "💡")

def mood_react(mood, bpm):
    color = react_to_audio(mood, int(bpm))
    say(f"[MOOD] {mood} \u2192 LED color: {color}", "🎛️")

def register():
    return {
        "glow": glow,
        "pulse": pulse,
        "led.mood_react": mood_react,
    }
