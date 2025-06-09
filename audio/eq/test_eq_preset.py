import json
import argparse
import matplotlib.pyplot as plt
import os
from live_eq_stream import semantic_gain_level

def load_eq_preset(preset_name, preset_file="audio/eq/eq_presets.json"):
    with open(preset_file, "r") as f:
        presets = json.load(f)

    if preset_name not in presets:
        raise ValueError(f"Preset '{preset_name}' not found in {preset_file}")

    preset = presets[preset_name]

    for band in preset:
        gain = band["gain_db"]
        if isinstance(gain, str):
            band["gain_db"] = semantic_gain_level(gain)

    return preset

def plot_preset(preset, title):
    freqs = [band["freq"] for band in preset]
    gains = [band["gain_db"] for band in preset]

    plt.figure(figsize=(10, 4))
    plt.plot(freqs, gains, marker="o", linestyle="-")
    plt.title(f"EQ Preset: {title}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Test and visualize EQ presets.")
    parser.add_argument("preset", help="Name of the preset to load (from eq_presets.json)")
    parser.add_argument("--plot", action="store_true", help="Plot the preset response curve")

    args = parser.parse_args()

    try:
        preset = load_eq_preset(args.preset)
        print (f"\n[  Loaded Preset: {args.preset}  ]")
        for band in preset:
            print (f"  - Freq: {band['freq']} Hz | Q: {band['q']} | Gain: {band['gain_db']} dB")

        if args.plot:
            plot_preset(preset, args.preset)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main() 
