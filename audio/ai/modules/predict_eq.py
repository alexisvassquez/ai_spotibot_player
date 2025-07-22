# ai_spotibot_player
# AudioMIX
# audio/ai/modules/predict_eq.py

import torch
import numpy as np
import librosa
import sys
from audio.ai.modules.lightning_module import LightningEQNet

LABELS_PATH = "models/eq_labels.txt"
MODEL_PATH = "models/eq_model.pt"

def extract_features(filepath):
    y, sr = librosa.load(filepath, duration=10, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    return np.hstack([np.mean(mfcc, axis=1), np.mean(contrast, axis=1)])

def load_labels():
    with open(LABELS_PATH, "r") as f:
        return f.read().strip().split(",")

def predict(filepath):
    print (f"🎧 Analyzing: {filepath}")
    features = extract_features(filepath)
    x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

    labels = load_labels()
    model = LightningEQNet(input_dim=20, num_classes=len(labels))
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    with torch.no_grad():
        output = model(x).squeeze(0).numpy()

    predictions = {label: float(score) for label, score in zip(labels, output)}
    sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

    print ("\n🎛️ Predicted EQ Tags:")
    for label, score in sorted_preds:
        status = "✅" if score > 0.5 else "❌"
        print (f"{status} {label:<10} -> confidence: {score:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: python3 audio/ai/modules/predict_eq.py <path_to_audio_file>")
        sys.exit(1)

    predict(sys.argv[1])
