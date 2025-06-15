import librosa

def get_bpm_from_audio(file_path):
    try:
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return int(tempo)
    except Exception as e:
        print (f"[!] BPM detection failed: {e}")
        return 120 # Fallback default BPM
