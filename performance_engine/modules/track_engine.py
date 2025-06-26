import subprocess

track_registry = {}

class Track:
    def __init__(self, name):
        self.name = name
        self.clips = []
        self.volume = 1.0
        self.muted = False
        self.eq_settings = {}

    def add_clip(self, clip_path):
        self.clips.append(clip_path)

    def set_volume(self, level):
        self.volume = float(level)

    def mute(self, state=True):
        self.muted = state

    def __repr__(self):
        return f"<Track {self.name} | Volume: {self.volume:.2f} | Muted: {self.muted}>"

# === DSL Command Functions ===

def add_track(name):
    if name in track_registry:
        return f"Track '{name}' already exists."
    track_registry[name] = Track(name)
    return f"👌 Track '{name}' created."

def add_clip(track_name, clip_path):
    track = track_registry.get(track_name)
    if not track:
        return f"❌ Track '{track_name}' not found."
    track.add_clip(clip_path)
    return f"🎵 Added clip to '{track_name}': {clip_path}"

def set_volume(track_name, level):
    track = track_registry.get(track_name)
    if not track:
        return f"❌ Track '{track_name}' not found."
    track.set_volume(level)
    return f"🔊 Volume set for '{track_name}': {level}"

def mute_track(track_name, state="True"):
    track = track_registry.get(track_name)
    if not track:
        return f"❌ Track '{track_name}' not found."
    track.mute(state.lower() == "true")
    return f"🔇 Muted: {track_name} = {track.muted}"

def play_clip(path):
    subprocess.run(["aplay", path])

# === AudioScript Command Registration ===

def register():
    return {
        "add_track": add_track,
        "add_clip": add_clip,
        "set_volume": set_volume,
        "mute_track": mute_track,
        "play_clip": play_clip
    }
