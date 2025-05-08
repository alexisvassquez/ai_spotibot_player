import librosa
import json
import sys
import numpy as np
# import sounddevice as sd
from pydub import AudioSegment
import tempfile
import os
import time

def convert_to_wav(input_path):
    audio = AudioSegment.from_file(input_path) # Load original file (mp3, flac, etc.)
    audio = audio.set_frame_rate(44100).set_channels(2).normalize() # Normalize + ensure consistent sample rate/channel format
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav: # Export to temp .wav file
        audio.export(temp_wave.name, format="wav")
        return temp_wav.name

def analyze(file_path, sr=22050, duration=None, hop_length=1024, verbose=True):
    wav_path = convert_to_wav(file_path)
    y, sr = librosa.load(wav_path, sr=None)

    start_time = time.time()

    y, sr = librosa.load(file_path, sr=sr, duration=duration)
    if verbose:
        print (f"[INFO] Loaded {file_path} | Duration: {librosa.get_duration(y=y, sr=sr): .2f}s | Sample Rate: {sr}")

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    spectral = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=hop_length)

    result = {
        "filename": file_path,
        "tempo": float(tempo) if np.ndim(tempo) == 0 else float(tempo[0]),
	"mfcc_mean": mfcc.mean(axis=1).tolist(),
	"spectral_contrast_mean": spectral.mean(axis=1).tolist()
    }

    if verbose:
        print (f"[INFO] Tempo: {float(tempo):.2f} BPM")
        print (f"[INFO] MFCC shape: {mfcc.shape}")
        print (f"[INFO] Spectral Contrast shape: {spectral.shape}")
        print (f"[INFO] Analysis completed in {time.time() - start_time:.2f}s")

    return result, y, sr

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: python3 analyze_audio.py /home/wholesomedegenerate/ai_spotibot_player/audio/samples/cvltiv8r_clean.wav")
        sys.exit(1)

    path = sys.argv[1]
    data, y, sr = analyze(path)

    print (json.dumps(data, indent=2))

# After loading audio with librosa
def fallback_play(path):
    try:
        print (f"[INFO] Playing audio using ffplay...")
        os.system(f"ffplay -nodisp -autoexit \"{path}\"")
    except Exception as e:
        print (f"[ERROR] Failed to play audio: {e}")

    if "--play" in sys.argv:
        fallback_play(path)
