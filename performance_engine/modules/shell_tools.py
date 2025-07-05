from time import sleep
from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry
from audio.led.controller import LightController

led = LightController()
current_zone = "main"

def list_commands(*args):
    say("Available AudioScript Commands:", "🃏")
    if not command_registry:
        say("⚠️ Registry is empty!")
    else:
        for cmd in sorted(command_registry.keys()):
            say(f" - {cmd}")

def set_static_color(color):
    led.set_color(color, zone=current_zone)
    say(f"[LED] Static {color} set on {current_zone}", "🌈")

def fade_color(color, duration):
    try:
        duration = float(duration)
        led.fade_to(color, duration, zone=current_zone)
        say(f"[LED] Fading to {color} over {duration}s on {current_zone}"),
    except ValueError:
        say(f"[ERROR] Invalid duration for fade()", "❌")

def delay_seconds(seconds):
    try:
        seconds = float(seconds)
        say(f"[WAIT] Sleeping for {seconds} seconds...", "🕛")
        sleep(seconds)
    except ValueError:
        say("[ERROR] Invalid delay duration", "❌")

def set_active_zone(zone_name):
    global current_zone
    current_zone = zone_name
    say(f"[ZONE] Active LED zone set to: {current_zone}", "🌎")

def register():
    return {
        "list_commands": list_commands,
        "color": set_static_color,
        "fade": fade_color,
        "delay": delay_seconds,
        "set_zone": set_active_zone
    }
