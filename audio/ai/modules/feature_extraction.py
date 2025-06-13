import librosa
import numpy as np
import time

def extract_features(file_path, sr=22050, duration=None, hop_length=1024, verbose=True):
    y, sr = librosa.load(file_path, sr=sr, duration=duration)
    features = {}
    if verbose:
        print(f"[INFO] Loaded {file_path} | Duration: {librosa.get_duration(y=y, sr=sr):.2f}s | Sample Rate: {sr}")

    start_time = time.time()

    # MFCCs
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features["mfcc_mean"] = mfcc.mean(axis=1).tolist()    
    features["mfcc_var"] = mfcc.var(axis=1).tolist()

    # Spectral Contrast
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    features["spectral_contrast_mean"] = contrast.mean(axis=1).tolist()
    features["spectral_contrast_var"] = contrast.var(axis=1).tolist()

    # Spectral Bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    features["spectral_bandwidth"] = {
        "mean": spectral_bandwidth.mean(axis=1).tolist(),
        "var": spectral_bandwidth.var(axis=1).tolist(),
    }

    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    features["tempo"] = tempo

    elapsed_time = time.time() - start_time

    return features
