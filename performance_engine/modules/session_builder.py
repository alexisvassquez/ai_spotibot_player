# ai_spotibot_player
# AudioMIX
# performance_engine/modules/session_builder.py

import json
from pathlib import Path

# Track represents a single audio or MIDI track in a session
class Track:
    def __init__(self, file_path, start=0.0, volume=0.0, pan=0.0, track_type='audio'):
        # save track metadata
        self.file_path = Path(file_path)    # path to file (audio or MIDI)
        self.start = float(start)           # start time on timeline (measured in secs)
        self.volume = float(volume)         # track volume in dB
        self.pan = float(pan)               # stereo pan (-1.0 left to +1.0 right)
        self.type = track_type              # track type (audio file, midi, synth, etc.)

    def to_dict(self):
        # convert to dictionary for json export
        return {
            "file": str(self.file_path),    # string format
            "start": self.start,
            "volume": self.volume,
            "pan": self.pan,
            "type": self.type
        }

# AudioSession represents the full multi-track session timeline
class AudioSession:
    def __init__(self):
        self.tracks = []    # list of track objs

    def add_track(self, file_path, start=0.0, volume=0.0, pan=0.0, track_type='audio'):
        # add a new track to the session
        self.tracks.append(Track(file_path, start, volume, pan, track_type))

    def list_tracks(self):
        # return all tracks as list of dictionaries
        return [track.to_dict() for track in self.tracks]

    def save(self, path):
        # save session to json file
        with open(path, "w") as f:
            json.dump({"tracks": self.list_tracks()}, f, indent=2)    # json prettier format

    def load(self, path):
        # load session from json file
        with open(path, "r") as f:
            data = json.load(f)
            self.tracks = [Track(**track) for track in data["tracks"]]

    def __str__(self):
        # return pretty-printed track listing
        return "\n".join(
            f"{i+1}. {track.file_path.name} ({track.type}) @ {track.start}s, vol={track.volume}, pan={track.pan}"
            for i, track in enumerate(self.tracks)
        )

# For testing in CLI environment
if __name__ == "__main__":
    session = AudioSession()
    session.add_track("audio/samples/full/ilariio_soft-chill-vibes.mp3", start=0.0, volume=-2.0)
    session.add_track("audio/samples/full/cvltiv8r_clean.wav", start=1.5, volume=-1.0)
    print ("🎚️  Current Tracks in Session:")
    print (session)
