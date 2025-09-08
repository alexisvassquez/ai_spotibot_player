# ai_spotibot_player
# AudioMIX
# audioscript_runtime.py

import sys
import readline
import os
import importlib
import shlex
import atexit
import time
from performance_engine.modules.context import command_registry
from audio.ai.inference_engine import generate_lighting_profile
from performance_engine.modules import fade_mod
from performance_engine.modules.shell_tools import load_dynamic_commands
load_dynamic_commands()

# Enable persistent shell history
histfile = os.path.expanduser("~/.audioscript_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass
atexit.register(readline.write_history_file, histfile)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

USE_EMOJIS = True
USE_SYMBOLS = True
VERBOSE = False # Set to True for debugging logs
 
def load_modules():
    module_dir = "performance_engine/modules"
    for file in os.listdir(module_dir):
        if file.endswith(".py") and not file.startswith("__"):
            mod_path = f"performance_engine.modules.{file[:-3]}" # dot-path
            mod_path = mod_path.replace("-", "_") # for safety
            module = importlib.import_module(mod_path)
            try:
                module = importlib.import_module(mod_path)
                if hasattr(module, "register"):
                    registered = module.register()
                    if registered:
                        if VERBOSE:
                            say(f"Registering from {file}: {list(registered.keys())}", "🧠")
                        command_registry.update(registered)
                        command_registry["trigger_zones"] = trigger_zones
                    elif VERBOSE:
                        say(f"⚠️ {file} register() returned nothing", "❓")
                elif VERBOSE:
                    say(f"⚠️ No register() in {file}", "🚫")
            except Exception as e:
                if VERBOSE:
                    say(f"❌ Failed to import {file}: {e}", "💥")

def say(text, emoji=""):
    from audioscript_runtime import USE_EMOJIS, USE_SYMBOLS

    # Replace visual symbols with Unicode-safe versions
    if USE_EMOJIS and emoji:
        text = text.replace("->", "\u2192")
        text = text.replace("=>", "\u21D2")
        text = text.replace("<-", "\u2190")

    if USE_EMOJIS and emoji:
        print (f"{emoji} {text}")
    else:
        print (text)

def glow(color):
    say(f"[LED] glowing {color}", "💡")

def play(track):
    say(f"Now playing: {track}", "🔊")

def pulse(color, bpm):
    say(f"[LED] pulsing {color} @ {bpm} BPM", "💡")

def mood_set(mood):
    say(f"[MOOD] context set to: {mood}", "🎼")

def trigger_zones(zones, mood="calm", bpm=120):
    try:
        generate_lighting_profile({mood}, bpm=bpm, zones=zones)
        say(f"[LIGHTING] Triggered zones: {zones} | Mood: {mood} | BPM: {bpm}", "🌈")
    except Exception as e:
        say(f"[ERROR] Lighting trigger failed: {e}", "❌")

# Basic Command Parser
def parse_and_execute(line):
    line = line.strip()
    if line.strip() == "test_lines":
        return [
            print ("[TEST] Line 1"),
            print ("[TEST] Line 2")
        ]

    if line.startswith("#") or not line:
        return # ignore comments and blank lines

    if "(" in line and line.endswith(")"):
        command, arg_str = line.split("(", 1)
        arg_str = arg_str[:-1] # Remove trailing ")"

        if "@" in arg_str:
            parts = shlex.split(arg_str)
        else: 
            parts = shlex.split(arg_str)

        func = command_registry.get(command)
        if func:
            try:
                result = func(parts)
                if isinstance(result, list):
                    for line in result:
                        say(line)
                elif isinstance(result, str):
                    say(result)
                elif result is not None:
                    say(str(result))
            except Exception as e:
                say(f"[ERROR] Execution failed: {e}", "❌")
        else:
            say(f"[ERROR] Unknown command: {command}", "⚠️")
    else:
        say(f"[ERROR] Invalid syntax: {line}", "❕")

# Interactive Loop
def main():
    global USE_EMOJIS, USE_SYMBOLS
    import sys

    if "--no-emoji" in sys.argv:
        USE_EMOJIS = False
    if "--no-symbols" in sys.argv:
        USE_SYMBOLS = False
    if "--debug" in sys.argv:
        VERBOSE = False

    # Load command modules after global settings are set
    load_modules()

    say("Welcome to AudioMIX - AudioScript Shell v0.1", "🎚️")
    say("Type AudioScript commands below. Ctrl+C to exit.\\n")

    # Check for script file
    for arg in sys.argv[1:]:
        if arg.endswith(".audioscript") or arg.endswith(".as"):
            say(f"Running AudioScript file: {arg}", "▶️")
            with open(arg, "r") as f:
                for line in f:
                    parse_and_execute(line.strip())
            return

    midi_tick = command_registry.get("midi_tick")
    # Interactive loop
    while True:
        try:
            if midi_tick:
                midi_tick()    # keep processing realtime MIDI events
            line = input("🎛️ > ")
            parse_and_execute(line)
        except KeyboardInterrupt:
            say("Exiting AudioMIX Shell. Goodbye 👋", "🛑")
            break
        except Exception as e:
            say(f"[AS Shell Error] {e}", "❌")
            time.sleep(0.01)

if __name__ == "__main__":
    main()
