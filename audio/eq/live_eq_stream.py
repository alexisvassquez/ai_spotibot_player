import pyaudio
import numpy as np
import json
import scipy.signal as signal
import os

# === Load EQ Presets ===
def load_eq_preset(preset_name, preset_file="audio/eq/eq_presets.json"):
    with open(preset_file, "r") as f:
        presets = json.load(f)
    return presets.get(preset_name, [])

# === Design Biquad Filters ===
def create_filterbank(preset, fs, order=2):
    filters = []
    for band in preset:
        f0 = band["freq"]
        q = band["q"]
        gain = band["gain_db"]
        b, a = signal.iirpeak(f0, q, fs=fs) if gain >= 0 else signal.iirnotch(f0, q, fs=fs)
        b *= 10**(gain / 40) # Adjust gain
        filters.append((b, a))
    return filters

# === Apply Filters to Chunk ===
def apply_filters(chunk, filters):
    output = chunk
    for b, a in filters:
        output = signal.lfilter(b, a, output)
    return output

# === Real-time Audio Stream with EQ ===
def stream_with_eq(preset_name="vocal_clarity"):
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    preset = load_eq_preset(preset_name)
    filters = create_filterbank(preset, fs=RATE)

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    print(f"[INFO] Streaming with preset: {preset_name}")
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            filtered = apply_filters(audio_data, filters)
            stream.write(filtered.astype(np.float32).tobytes())
    except KeyboardInterrupt:
        print("\[INFO] Stream stopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    stream_with_eq("vocal_clarity") # Change to "bass_boost", etc.
