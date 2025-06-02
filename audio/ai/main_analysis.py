import json
import sys
import numpy as np
import os
from audio.ai.modules.convert_audio import convert_to_wav
from audio.ai.modules.feature_extraction import extract_features

def convert_ndarrays(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarrays(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarrays(i) for i in obj]
    else:
        return obj

def analyze(file_path):
    wav_path = convert_to_wav(file_path)
    features = extract_features(wav_path)
    features_clean = convert_ndarrays(features)

    output_dir = "audio/analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    # Save to JSON file
    json_path = os.path.join(output_dir, "features_summary.json")
    with open(json_path, "w") as f:
        json.dump(features_clean, f, indent=2)

    return features_clean

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: python3 main_analysis.py <audio_file>")
        sys.exit(1)

    result = analyze(sys.argv[1])
    print (json.dumps(result, indent=2))
