USE_EMOJIS = True

def say(text, emoji=""):
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

# Registry maps script calls to Python functions
command_registry = {
    "glow": glow,
    "play": play,
    "pulse": pulse,
    "mood.set": mood_set,
}

# Basic Command Parser
def parse_and_execute(line):
    line = line.strip()
    if line.startswith("mood.set("):
        arg = line[len("mood.set("):-1].strip('"')
        mood_set(arg)
    elif line.startswith("glow("):
        arg = line[len("glow("):-1].strip('"')
        glow(arg)
    elif line.startswith("play("):
        arg = line[len("play("):-1].strip('"')
        play(arg)
    elif line.startswith("pulse("):
        inside = line[len("pulse("):-1]
        color, bpm = [x.strip().strip('"') for x in inside.split(",")]
        pulse(color, int(bpm))
    else:
        say(f"[ERROR] Unknown command: {line}", "⚠️")

# Interactive Loop
def main():
    global USE_EMOJIS
    import sys
    if "--no-emoji" in sys.argv:
        USE_EMOJIS = False

    say("Welcome to AudioMIX - AudioScript Shell v0.1", "🎚️")
    say("Type AudioScript commands below. Ctrl+C to exit.\\n")

    while True:
        try:
            line = input("🎛️ > ")
            parse_and_execute(line)
        except KeyboardInterrupt:
            say("Exiting AudioMIX Shell. Goodbye 👋", "🛑")
            break

if __name__ == "__main__":
    main()
