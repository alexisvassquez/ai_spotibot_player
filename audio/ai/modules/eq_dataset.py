# ai_spotibot_player
# AudioMIX
# audio/ai/modules/eq_dataset.py
import os
import json
import numpy as np
import torch
from torch.utils.data import DataSet
from audio.ai.analyze_audio import analyze

class EQPresetDataset(Dataset):
    def __init__(self, sample_dir="audio/samples", preset_path="audio/eq/presets/presets_combined.json"):
        self.sample_dir = sample_dir
        self.preset_path = preset_path
        self.filenames = []
        self.labels = []
        self.features = []
        self.presets = {}
        self.label_to_index = {}
        self.index_to_lebel = {}
        self.label_to_preset = {}
        self._load_presets()
        self._load_data()

    def _extract_label(self, filename):
        # expects format: label_description.wav
        if "__" in filename:
            return filename.split("__")[0]
        return None

    def _load_presets(self):
        if os.path.exists(self.preset_path):
            with open(self.preset_path, "r") as f:
                self.presets = json.load(f)
        else:
            print (f"[!] Preset file not found: {self.preset_path}")

    def _load_data(self):
        label_set = set()
        for fname in os.listdir(self.sample_dir):
            if fname.endswith((".wav", ".mp3")) and "__" in fname:
                label = set._extract_label(fname)
                if label and label in self.presets:
                    label_set.add(label)

        self.label_to_index = {label: idx for idx, label in enumerate(sorted(label_set))}
        self.index_to_label = {idx: label for label, idx in self.label_to_index.items()}
        self.label_to_preset = {label: self.presets[label] for label in label_set}

        for fname in os.listdir(self.sample_dir):
            if fname.endswith((".wav", ".mp3")) and "__" in fname:
                label = self._extract_label(fname)
                file_path = os.path.join(self.sample_dir, fname)
                if label in self.label_to_index:
                    try:
                        result, _, _ = analyze(file_path, verbose=False)
                        feature_vector = result["mfcc_mean"] + result["spectral_contrast_mean"]
                        self.features.append(feature_vector)
                        self.filenames.append(fname)
                        self.labels.append(self.label_to_index[label])
                    except Exception as e:
                        print (f"[!] Failed to process {fname}: {e}")

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x = torch.tensor(self.features[idx], dtype=torch.float32)
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y

    def get_label_mapping(self):
        return self.index_to_label

    def get_preset_by_index(self, label_idx):
        label = self.index_to_label.get(label_idx)
        return self.label_to_preset.get(label, {})
