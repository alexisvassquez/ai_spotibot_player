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

def load_labels():
    with open(LABELS_PATH, "r") as f:
        return f.read().strip().split(",")

def flatten_features_dict(features_dict):
    flat = []
    for key, value in features_dict.items():
        if isinstance(value, dict):    # nested mean/var
            flat.extend(value.get("mean", []))
            flat.extend(value.get("var", []))
        elif isinstance(value, (list, np.ndarray)):
            flat.extend(value)
        elif isinstance(value, (int, float)):
            flat.append(value)
        else:
            print (f"[⚠️] Skipping unsupported feature type: {key}")
    return flat

def predict_labels(features_dict):
    labels = load_labels()
    flat_features = flatten_features_dict(features_dict)

    # Handle input features 
    x = torch.tensor(flat_features, dtype=torch.float32).unsqueeze(0)

    # Load Lightning model
    model = LightningEQNet(input_dim=len(flat_features), num_classes=len(labels))
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    with torch.no_grad():
        output = model(x).squeeze(0).numpy()

    predictions = {label: float(score) for label, score in zip(labels, output)}
    sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

    print ("\n🎛️ Predicted EQ Tags:")
    selected_labels = []
    for label, score in sorted_preds:
        status = "✅" if score > 0.5 else "❌"
        print (f"{status} {label:<10} -> confidence: {score:.2f}")
        if score > 0.5:
            selected_labels.append(label)

    return selected_labels

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: python3 -m audio.ai.modules.predict_eq <audio_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    from audio.ai.modules.feature_extraction import extract_features
    features = extract_features(file_path)

    if not features:
        print ("[❌] Failed to extract features.")
        sys.exit(1)

    print (f"[+] Extracted features from {file_path}")
    tags = predict_labels(features)

    print ("\🎧 Final EQ Tags Selected:", tags)
