# ai_spotibot_player
# AudioMIX
# audio/analysis_output/generate_audio_features.py

import os
import json
import librosa
import numpy as np

# Define paths and labels
samples = {
    "audio/samples/cvltiv8r_clean.wav": ["bass_boost", "treble"],
    "audio/samples/ilariio_soft-chill-vibes.mp3": ["bass_boost", "mids_cut"]
}

features_output = []
labels_output = {}

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Extract features
for filepath, labels in samples.items():
    try:
        y, sr = librosa.load(filepath, sr=22050)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean(axis=1)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Aggregate into feature vector
        feature_vector = {
            "filename": os.path.basename(filepath),
            "mfcc": mfcc.tolist(),
            "spectral_contrast": spectral_contrast.tolist(),
            "tempo": float(tempo)
        }

        features_output.append(feature_vector)
        labels_output[os.path.basename(filepath)] = labels

    except Exception as e:
        print (f"Error processing {filepath}: {e}")

# Save features and labels
with open("data/audio_features.json", "w") as f:
    json.dump(features_output, f, indent=2)

with open("data/eq_labels.json", "w") as f:
    json.dump(labels_output, f, indent=2)
