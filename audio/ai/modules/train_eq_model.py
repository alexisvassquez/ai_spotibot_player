# ai_spotibot_player
# AudioMIX
# audio/ai/modules/train_eq_model.py

import sys
import os
import torch
import numpy as np
import librosa
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from sklearn.preprocessing import MultiLabelBinarizer
from audio.ai.modules.lightning_module import LightningEQNet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

# Paths
SAMPLES = {
    "audio/samples/cvltiv8r_clean.wav": ["bass_boost", "treble"],
    "audio/samples/ilariio_soft-chill-vibes.mp3": ["bass_boost", "mids_cut"]
}

# Feature Extraction
def extract_features(path):
    y, sr = librosa.load(path, duration=10, sr=22050)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    return np.hstack([np.mean(mfcc, axis=1), np.mean(spectral_contrast, axis=1)])

# PyTorch Dataset
class EQDataset(Dataset):
    def __init__(self, samples, label_binarizer):
        self.features = []
        self.labels = []
        for path, tags in samples.items():
            feats = extract_features(path)
            self.features.append(feats)
            self.labels.append(label_binarizer.transform([tags])[0])

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x = torch.tensor(self.features[idx], dtype=torch.float32)
        y = torch.tensor(self.labels[idx], dtype=torch.float32)
        return x, y

# Main Training Function
def train_model():
    all_labels = list({label for taglist in SAMPLES.values() for label in taglist})
    mlb = MultiLabelBinarizer(classes=all_labels)
    mlb.fit([all_labels])

    dataset = EQDataset(SAMPLES, mlb)
    train_loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = LightningEQNet(input_dim=20, num_classes=len(all_labels))

    trainer = pl.Trainer(max_epochs=100, logger=False, enable_checkpointing=False)
    trainer.fit(model, train_loader)

    # Save model and label binarizer
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/eq_model.pt")
    with open("models/eq_labels.txt", "w") as f:
        f.write(",".join(mlb.classes_))

    print ("✅ EQ model trained and saved.")

if __name__ == "__main__":
    train_model()
