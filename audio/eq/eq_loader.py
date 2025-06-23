# audio/eq/eq_loader.py
import os
import json
import yaml

# Load a single EQ preset file (JSON or YAML)
def load_eq_preset(filename):
    base_dir = os.path.dirname(os.path.realpath(__file__))

    # Build full path to presets/
    preset_path = os.path.join(base_dir, "presets", filename)

    print(f"[DEBUG] Loading EQ presets from: {preset_path}")

    ext = os.path.splitext(preset_path)[1].lower()

    with open(preset_path, 'r') as f:
        if ext == ".json":
            data = json.load(f)
        elif ext in [".yaml", ".yml"]:
            data = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported preset format: {ext}")

    return validate_presets(data)

# Validate and return a full presets dictionary
def validate_presets(data):
    for name, preset in data.items():
        if "filters" not in preset:
            raise ValueError(f"Preset: '{name}' missing required 'filters' key.")
        for i, filt in enumerate(preset["filters"]):
            if not all(k in filt for k in ("freq", "q", "gain_db")):
                raise ValueError(f"Filter at index {i} in preset '{name}' missing keys.")
            if not isinstance(filt["freq"], (int, float)) or \
                not isinstance(filt["q"], (int, float)) or \
                not isinstance(filt["gain_db"], (int, float)):
                    raise ValueError(f"Filter at index {i} in preset '{name}' has invalid types.")
    return data

# Utility: load all presets from a directory (JSON/YAML files)
def load_all_presets(presets_dir):
    all_presets = {}
    for filename in os.listdir(presets_dir):
        if filename.endswith(('.json', '.yaml', '.yml')):
            full_path = os.path.join(presets_dir, filename)
            try:
                data = load_eq_preset(full_path)
                all_presets.update(data)
            except Exception as e:
                print (f"[WARN] Skipped '{filename}': {e}")
    return all_presets
