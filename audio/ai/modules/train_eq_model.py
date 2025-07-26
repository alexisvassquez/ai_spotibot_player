# ai_spotibot_player
# AudioMIX
# audio/ai/modules/train_eq_model.py

import sys
import os
import json
import torch
import pytorch_lightning as pl
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MultiLabelBinarizer
from audio.ai.modules.lightning_module import LightningEQNet
from audio.ai.modules.predict_eq import flatten_features_dict
import librosa
import numpy as np

USE_PRECOMPUTED = True    # toggle to False for dynamic extraction

# Paths
SAMPLES = "audio/samples/"
FEATURES_PATH = "audio/analysis_output/data/audio_features.json"
LABELS_PATH = "audio/analysis_output/data/eq_labels.json"
MODEL_SAVE_PATH = "models/eq_model.pt"
OUTPUT_LABELS_TXT = "models/eq_labels.txt"

# Feature Extraction
def extract_features(filepath):
    y, sr = librosa.load(filepath, duration=10, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    tempo = librosa.beat.tempo(y=y, sr=sr)

    return {
        "mfcc_mean": np.mean(mfcc, axis=1).tolist(),
        "mfcc_var": np.var(mfcc, axis=1).tolist(),
        "spectral_contrast_mean": np.mean(spectral_contrast, axis=1).tolist(),
        "spectral_contrast_var": np.var(spectral_contrast, axis=1).tolist(),
        "spectral_bandwidth": {
            "mean": [np.mean(spectral_bandwidth)],
            "var": [np.var(spectral_bandwidth)]
        },
        "tempo": tempo
    }

# PyTorch Dataset
class EQDataset(Dataset):
    def __init__(self, mlb, use_precomputed=True):
        self.data = []
        self.labels = []

        with open(LABELS_FILE, "r") as f:
            label_dict = json.load(f)

        if use_precomputed:
            with open(FEATURES_FILE, "r") as f:
                raw_features = json.load(f)

            # Flatten list of single-entry dicts into one combined dict
            feature_dict = {}
            for entry in raw_features:
                if isinstance(entry, dict):
                    for k, v in entry.items():
                        feature_dict[k.strip().lower()] = v

            for filename, tags in label_dict.items():
                normalized_name = filename.strip().lower()
                if normalized_name not in feature_dict:
                    print (f"[WARN] Missing features for: {filename}")
                    continue
                flat = flatten_features_dict(feature_dict[normalized_name])
                self.data.append(flat)
                self.labels.append(tags)
        else:
            for filename, tags in label_dict.items():
                filepath = os.path.join(SAMPLES_DIR, filename)
                if not os.path.exists(filepath):
                    print (f"[WARN] Missing file: {filepath}")
                    continue
                features = extract_features(filepath)
                flat = flatten_features_dict(features)
                self.data.append(flat)
                self.labels.append(tags)

        self.data = torch.tensor(self.data, dtype=torch.float32)
        self.labels = torch.tensor(mlb.fit_transform(self.labels), dtype=torch.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Main Training Function
def train_model():
    with open(LABELS_FILE, "r") as f:
        all_labels = set(tag for tags in json.load(f).values() for tag in tags)
    labels = sorted(list(all_labels))
    with open(OUTPUT_LABELS_TXT, "w") as f:
        f.write(",".join(labels))

    mlb = MultiLabelBinarizer(classes=labels)
    dataset = EQDataset(mlb, use_precomputed=USE_PRECOMPUTED)

    print (f"✅ Loaded {len(dataset)} samples for training")
    if len(dataset) == 0:
        raise RuntimeError("⚠️  No data available for training. Check matching keys in labels vs features.")

    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = LightningEQNet(input_dim=dataset.data.shape[1], num_classes=len(labels))
    trainer = pl.Trainer(max_epochs=30, accelerator="cpu", logger=False, enable_checkpointing=False)
    trainer.fit(model, dataloader)

    # Save model and label binarizer
    torch.save(model.state_dict(), MODEL_FILE)
    print ("✅ EQ model trained and saved to {MODEL_FILE}.")

if __name__ == "__main__":
    train_model()
