from performance_engine.modules.shared import say
from performance_engine.modules.context import command_registry
from audio.eq.equalizer import (
    set_band, 
    reset_eq, 
    load_preset, 
    save_preset, 
    get_status,
    set_eq_mode,
    get_eq_mode
)
from audio.eq.eq_loader import load_eq_preset
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
    current_mode = get_eq_mode()
    say(f"EQ Mode: {current_mode.upper()}", "🔉")
    say("Current EQ Settings:", "📊")
    for band, gain in status.items():
        say(f" - {band}: {gain} dB")

def eq_mode_set(args):
    mode = args.strip().lower()
    if mode not in ["semantic", "filter"]:
        say("Usage: eq.mode(semantic) or eq.mode(filter)", "🔉")
        return

    set_eq_mode(mode)
    say(f"Switched EQ mode to: {mode.upper()}", "🧠")

# At module level (load once)
PRESETS = load_eq_preset("presets_combined.json")

def eq_preset(args):
    preset_name = args.strip()
    if preset_name in PRESETS:
        filters = PRESETS[preset_name]["filters"]
        load_preset(filters) # Applies gain per band under the hood
        say(f"Loaded EQ preset: {preset_name}", "🎧")
    else:
        say(f"[ERROR] Preset '{preset_name}' not found", "❌")

def eq_boost_semantic(tag, delta_gain):
    for name, preset in PRESETS.items():
        if "semantic" in preset and tag in preset["semantic"]:
            preset["semantic"][tag] += delta_gain
            say(f"Boosted '{tag}' by {delta_gain}dB in all relevant presets", "🔊")

def eq_list(_):
    say("Available EQ Presets:", "📊")
    for name in PRESETS.keys():
        say(f" - {name}")


# Registering commands
def register():
    return {
        "eq.set": eq_set,
        "eq.reset": eq_reset,
        "eq.status": eq_status,
        "eq.preset": eq_preset,
        "eq.mode": eq_mode_set,
        "eq.boost_semantic": eq_boost_semantic,
        "eq.list": eq_list
    }
