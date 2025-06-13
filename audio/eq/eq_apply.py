# audio/eq/eq_apply.py

import numpy as np
import soundfile as sf
from scipy.signal import iirpeak, lfilter

def apply_eq_filters(audio, sr, filters):
    processed = audio.copy()

    for f in filters:
        freq = f["freq"]
        q = f["q"]
        gain_db = f["gain_db"]

        # Convert gain from dB to linear
        gain = 10 ** (gain_db / 20)

        # Create peaking filter (IIR peak)
        b, a = iirpeak(freq / (sr / 2), q)

        # Apply gain
        b *= gain

        # Apply filter
        processed = lfilter(b, a, processed)

    return processed

def process_wav_file(input_path, output_path, filters):
    audio, sr = sf.read(input_path)

    # If stereo, process each channel independently
    if len(audio.shape) == 2:
        processed = np.zeros_like(audio)
        for ch in range(audio.shape[1]):
            processed[:, ch] = apply_eq_filters(audio[:, ch], sr, filters)
    else:
        processed = apply_eq_filters(audio, sr, filters)

    sf.write(output_path, processed, sr)
    print (f"✅ Processed file saved to: {output_path}")
