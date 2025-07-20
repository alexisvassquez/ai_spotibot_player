# ai_spotibot_player
# AudioMIX
# audio/analysis_output/plot_eq_presets.py
import json
import matplotlib.pyplot as plt
import os

# Path to the combined EQ presets file
base_dir = os.path.dirname(__file__)
preset_path = os.path.abspath(os.path.join(base_dir, "..", "eq", "presets", "presets_combined.json"))
output_image_path = os.path.abspath(os.path.join(base_dir, "..", "..", "docs", "plots", "eq_presets.png"))

# Ensure output directory exists
os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

# Load preset data
with open(preset_path, "r") as f:
    presets = json.load(f)

plt.figure(figsize=(10, 6))
plotted_count = 0

for label, config in presets.items():
    filters = config.get("filters", {})
    freqs = []
    gains = []

    # Support for list or dict
    if not isinstance(filters, list):
        print (f"[!] Skipping non-list filter structure for: {label}")
        continue

    for entry in filters:
        # Convert frequency keys as float ("60Hz" -> 60)
        try:
            freq = entry.get("freq")
            gain = entry.get("gain_db")
            hz = float(freq)
            db = float(gain)
            freqs.append(hz)
            gains.append(db)
        except ValueError:
            print (f"[!] Skipping invalid filter in {label}: {entry} ({e})")

    # Sort by frequency for cleaner plotting
    if freqs and gains:
        sorted_data = sorted(zip(freqs, gains))
        freqs_sorted, gains_sorted = zip(*sorted_data)
        print (f"[DEBUG] Plotting: {label} -> Freqs: {freqs_sorted}, Gains: {gains_sorted}")
        plt.plot(freqs_sorted, gains_sorted, marker="o", label=label)
        plotted_count += 1
    else:
        print (f"[!] No valid filters for: {label}")

plt.title("EQ Preset Curves")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB)")
plt.xscale("log")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(output_image_path)
plt.show()

print (f"[✅] EQ plot saved to: {output_image_path}")
print (f"[✅] Total presets plotted: {plotted_count}")
