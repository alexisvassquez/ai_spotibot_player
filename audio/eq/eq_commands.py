from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry
from audio.eq.equalizer import set_band, reset_eq, load_preset, save_preset, get_status
import json
import os

def eq_set(*args):
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0] # Unpack if it's a list

    if len(args) != 2:
        say(f"Usage: eq.set(band,value)", "🔉")
        return

    band, value = args
    try:
        value = float(value)
    except ValueError:
        say(f"Invalid value: {value}. Must be a number.", "❌")
        return

    set_band(band, value)
    say(f"Set {band} to {value} dB", "🎚️")

def eq_reset(_):
    reset_eq()
    say("EQ settings reset to 0 dB on all bands", "🔄")

def eq_status(_):
    status = get_status()
    say("Current EQ Settings:", "📊")
    for band, gain in status.items():
        say(f" - {band}: {gain} dB")

def eq_preset(args):
    preset_name = args.strip()
    preset_loaded = False

    # Fallback: hardcoded presets
    fallback_presets = {
        "bass_boost": {
            "sub_bass": 6,
            "bass": 4,
            "low_mid": 2
        },
        "vocal_clarity": {
            "mid": 3,
            "presence": 4,
            "brilliance": 2
        },
        "flat": {
            "sub_bass": 0,
            "bass": 0,
            "low_mid": 0,
            "mid": 0,
            "presence": 0,
            "brilliance": 0,
            "air": 0,
            "sparkle": 0,
            "ultra": 0
        }
    }

    try:    
        presets_path = os.path.join(os.path.dirname(__file__), "presets.json")
        with open(presets_path, "r") as f:
            presets = json.load(f)

        if preset_name in presets:
            load_preset(presets[preset_name])
            say(f"Loaded EQ preset: {preset_name}", "🎧")
            return
        else:
            say(f"[ERROR] Preset '{preset_name}' not found", "⚠️")
    except Exception as e:
        say(f"[ERROR] Couldn't load presets.json: {str(e)}", "❌")
    
    if preset_name in fallback_presets:
        load_preset(fallback_presets[preset_name])
        say(f"Loaded EQ preset (fallback): {preset_name}", "🎧")
    else:
        say(f"[ERROR] Preset '{preset_name}' not found", "❌")

# Registering commands
def register():
    return {
        "eq.set": eq_set,
        "eq.reset": eq_reset,
        "eq.status": eq_status,
        "eq.preset": eq_preset
    }
