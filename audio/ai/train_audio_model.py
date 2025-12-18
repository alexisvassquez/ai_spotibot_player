# ai_spotibot_player
# AudioMIX
# audio/ai/train_audio_model.py

import os
import json
import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MultiLabelBinarizer

# Local imports
from audio.ai.modules.merge_dataset import load_and_merge_datasets
from validate_dataset import main as validate_dataset

# Config
# ------------
DATASET_DIR = Path("audio/ai/datasets/")
ROOT_MODEL_DIR = Path("models")
MODEL_DIR = ROOT_MODEL_DIR / "juniper"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "mood_classifier.pt"

BATCH_SIZE = 8
EPOCHS = 25
LEARNING_RATE = 0.001
FEATURE_COLUMNS = ["bpm", "energy", "valence", "danceability"]
TARGET_COLUMN = "moods"

# Dataset Class
# -------------
class MoodDataset(Dataset):
    def __init__(self, df, mlb):
        self.X = torch.tensor(df[FEATURE_COLUMNS].values, dtype=torch.float32)
        self.y = torch.tensor(mlb.transform(df[TARGET_COLUMN]), dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Model Definition
# -------------
class JuniperMoodNet(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim),
            nn.Sigmoid(),    # for multi-label probabilities
        )

    def forward(self, X):
        return self.net(X)

# Helpers
# -------------
def info(msg): print (f"🟢  {msg}")
def warn(msg): print (f"⚠️  {msg}")
def error(msg): print (f"❌  {msg}")

# Training Pipeline
# -------------
def train_mood_model():
    print ("\n🎵  Training Juniper2.0 PyTorch Mood Classifier\n" + "=" * 55)

    # 1. Validate dataset
    try:
        validate_dataset()
    except SystemExit:
        pass

    # 2. Merge metadata + labels
    df = load_and_merge_datasets()
    if df.empty:
        warn("Dataset is empty - nothing to train.")
        return

    if TARGET_COLUMN not in df.columns:
        warn("Missing 'moods' column - cannot train.")
        return

    # 3. Preprocess
    df = df[df["reference_only"].astype(str).str.lower() != "true"]
    df[TARGET_COLUMN] = df[TARGET_COLUMN].apply(lambda X: X if instance(X, list) else [])

    mlb = MultiLabelBinarizer()
    df[TARGET_COLUMN] = mlb.fit_transform(df[TARGET_COLUMN]).tolist()

    dataset = MoodDataset(df, mlb)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # 4. Initialize model
    input_dim = len(FEATURE_COLUMNS)
    output_dim = len(mlb.classes_) if len(mlb.classes_) > 0 else 1
    model = JuniperMoodNet(input_dim, output_dim)
    criterion = nn.BCELOSS()
    optimizer = optim.Adam(model.paramets(), lr=LEARNING_RATE)

    # 5. Train loop
    info(f"Training on {len(dataset)} samples for {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for X_batch, y_batch in dataloader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print (f"Epoch [{epoch+1}/{EPOCHS}]  Loss: {avg_loss:.4f}")

    # 6. Save model
    torch.save(model.state_dict(), MODEL_PATH)
    info(f"✅  Model saved to {MODEL_PATH}")

    print ("\n✨  Training complete! Juniper2.0 now has a neural mood sense")


if __name__ == "__main__":
    train_mood_model()
