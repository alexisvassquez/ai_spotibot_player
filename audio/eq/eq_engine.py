import os
import librosa
import soundfile as sf
import numpy as np
import json
import sys

def apply_eq(y, sr, gains_db, freqs):
    import scipy.signal
    output = y.copy()
    for gain_db, freq in zip(gains_db, freqs):
        b, a = scipy.signal.iirpeak(freq / (0.5 * sr), Q=1.0, gain=gain_db)
        output = scipy.signal.lfilter(b, a, output)
    return output

def load_presets(preset_file):
    with open(preset_file, "r") as f:
        return json.load(f)

def main(audio_path, preset_name):
    y, sr = librosa.load(audio_path, sr=None)
    presets = load_presets("eq_presets.json")
    if preset_name not in presets:
        print(f"Preset '{preset_name}' not found.")
        return
    eq_settings = presets[preset_name]
    gains_db = eq_settings["gains"]
    freqs = eq_settings["freqs"]
    y_eq = apply_eq(y, sr, gains_db, freqs)
    sf.write("equalized_output.wav", y_eq, sr)
    print ("Equalized audio writtenm to equalized_output.wav")

if __name__ == "__main__"
    if len(sys.argv) != 3:
        print ("Usage: python eq_engine.py <audio_file> <preset_name>")
    else:
        main(sys.argv[1], sys.argv[2])

# Scaffold for eq_presets.json
eq_presets_json = '''\
{
    "flat": {
        "gains": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "freqs": [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    },
    "bass_boost": {
        "gains": [6, 5, 3, 0, -2, -3, -4, -4, -5, -6],
        "freqs": [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    },
    "vocal_clarity": {
        "gains": [-3, -2, -1, 0, 3, 5, 4, 3, 2, 1],
        "freqs": [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    }
}
'''

# Write files
with open(eq_engine_path, "w") as f:
    f.write(eq_engine_code)

with open(eq_presets_path, "w") as f:
    f.write(eq_presets_json)

"Equalizer module scaffolded successfully in /audio/eq/ - ready for testing and tuning." 
