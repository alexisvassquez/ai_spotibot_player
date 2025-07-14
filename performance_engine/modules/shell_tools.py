import importlib.util
import os
from time import sleep
from performance_engine.utils.shell_output import say
from performance_engine.modules.context import command_registry
from audio.led.controller import LightController

led = LightController()
current_zone = "main"

def load_dynamic_commands():
    module_dir = os.path.dirname(__file__)
    print (f"[shell_tools] Scanning module dir: {module_dir}")

    if not os.path.exists(module_dir):
        print (f"[ERROR] Module directory not found: {module_dir}")
        return

    for filename in os.listdir(module_dir):
        if filename.endswith(".py") and not filename.startswith("__") and filename != "shell_tools.py":
            filepath = os.path.join(module_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "command") and "name" in module.command:
                    name = module.command["name"]
                    command_registry[name] = module.command["run"]
                    print (f"[REGISTERED] {name} command from {filename}")
            except Exception as e:
                print (f"[shell_tools] [ERROR] Failed to load {filename}: {e}")

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

def fade_to(color, duration):
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
        "fade_to": fade_to,
        "delay": delay_seconds,
        "set_zone": set_active_zone
    }
