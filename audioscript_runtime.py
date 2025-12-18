# ai_spotibot_player
# AudioMIX
# audioscript_runtime.py

from __future__ import annotations
import sys, os, importlib, shlex, atexit, time
import readline
from performance_engine.modules.context import command_registry

# Allowlist -> SAFE_MODE (for lighter runtime load)
# Light modules only
SAFE_MODE = os.environ.get("AUDIOMIX_SAFE", "0") == "1"
SAFE_MODE_ALLOWLIST = {
    "context.py",
    "shell_tools.py",
    "clip_launcher.py",
    "provider_commands.py",
    "eq_commands.py",
    "led_controller.py",
    "shared.py",
}

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
VERBOSE = True # Set to True for debugging logs with --debug flag

def main():
    print ("main() reached!")

# Register commands to registry function
def register_command(name: str, func):
    command_registry[name] = func

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

# Module loader
def load_modules():
    module_dir = "performance_engine/modules"
    for file in os.listdir(module_dir):
        if not file.endswith(".py") and not file.startswith("__") and file != "__pycache__":
             continue

        if SAFE_MODE and file not in SAFE_MODE_ALLOWLIST:
            if VERBOSE: say(f"Safe mode: skipping {file}")
            continue

        # dot-path..for safety
        mod_path = f"performance_engine.modules.{file[:-3]}".replace("-", "_")
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

# Built-in AS functions
# Lazy imports
def glow(color):
    say(f"[LED] glowing {color}", "💡")

# Global playback state
# PLAYBACK_MODE = ("lossless" or "lossy", codec_key)
PLAYBACK_MODE = ("lossless", "wav")    # default

# mode: 'lossless' or 'lossy'
# codec: one of codec_sim.CODEC_MAP keys (ignored for lossless)
def set_mode(mode: str, codec: str = "mp3_320"):
    global PLAYBACK_MODE
    m = (mode or "").strip().lower()
    if m not in ("lossless", "lossy"):
        raise ValueError("set_mode: mode must be 'lossless' or 'lossy'")
    if m == "lossy":
        # Validate the codec upfront
        from audio.utils.codec_sim import parse_codec    # lazy
        parse_codec(codec)
        PLAYBACK_MODE = (m, codec)
        say(f"Playback mode set to LOSSY ({codec})", "🎚️")
    else:
        PLAYBACK_MODE = ("lossless", "wav")
        say("Playback mode set to LOSSLESS", "🎚️")

def get_mode():
    mode, codec = PLAYBACK_MODE
    if mode == "lossy":
        say(f"Current mode: LOSSY ({codec})", "🎚️")
    else:
        say("Current mode: LOSSLESS", "🎚️")

# AS commands ex: set_mode("lossy", codec="mp3_128")
register_command("set_mode", set_mode)
register_command("get_mode", get_mode)

# Load 'path', ensure internal WAV format. If mode is 'lossy', round-trip through codec.
# Hand off to existing low-latency playback (PortAudio)
def play(path: str, **kwargs):
    if SAFE_MODE:
        say(f"[SAFE] Would play: {path} (no audio processing in safe mode)")
        return

    #lazy
    from audio.ai.modules.convert_audio import ensure_internal
    from audio.utils.codec_sim import roundtrip_lossy

    mode, codec = PLAYBACK_MODE
    # normalize input to internal WAV32F
    internal_wav = ensure_internal(path, target_sr=48000)

    # if lossy, encode/decode to WAV32F
    try:
        if mode == "lossy":
            sim_wav = roundtrip_lossy(internal_wav, codec_key=codec, target_sr=48000)
            _do_play(sim_wav, **kwargs)
            try: os.remove(sim_wav)
            except OSError: pass
        else:
            _do_play(internal_wav, **kwargs)
    # clean up normalized wav if temp
    finally:
        try: os.remove(internal_wav)
        except OSError: pass

def _do_play(wav_path: str, **kwargs):
    say(f"Now playing: {os.path.basename(wav_path)}", "🔊")

def pulse(color, bpm):
    say(f"[LED] pulsing {color} @ {bpm} BPM", "💡")

def mood_set(mood):
    say(f"[MOOD] context set to: {mood}", "🎼")

def trigger_zones(zones, mood="calm", bpm=120):
    if SAFE_MODE:
        say(f"[SAFE] Would trigger zones={zones} mood={mood} bpm={bpm}")
        return
    try:
        from audio.ai.inference_engine import generate_lighting_profiles    # lazy
        generate_lighting_profile({mood}, bpm=bpm, zones=zones)
        say(f"[LIGHTING] Triggered zones: {zones} | Mood: {mood} | BPM: {bpm}", "🌈")
    except Exception as e:
        say(f"[ERROR] Lighting trigger failed: {e}", "❌")

# Command execution
def parse_and_execute(line):
    line = (line or "").strip()
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
                result = func(*parts)
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

# AS Shell loop
def main():
    global USE_EMOJIS, USE_SYMBOLS, VERBOSE, SAFE_MODE

    # CLI flags
    if "--no-emoji" in sys.argv:
        USE_EMOJIS = False
    if "--no-symbols" in sys.argv:
        USE_SYMBOLS = False
    if "--debug" in sys.argv:
        VERBOSE = True
    if "--safe" in sys.argv:
        SAFE_MODE = True

    # Load command modules after global settings are set
    load_modules()

    say("Welcome to AudioMIX - AudioScript Shell v0.1", "🎚️")
    say("Type AudioScript commands below. Ctrl+C to exit.\\n")

    # Run script file if passed
    for arg in sys.argv[1:]:
        if arg.endswith(".audioscript") or arg.endswith(".as"):
            say(f"Running AudioScript file: {arg}", "▶️")
            with open(arg, "r") as f:
                for line in f:
                    parse_and_execute(line.strip())
            return

    midi_tick = None if SAFE_MODE else command_registry.get("midi_tick")

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
