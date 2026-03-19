# ai_spotibot_player
# AudioMIX
# audio/analysis_output/plot_waveform.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("audio/analysis_output/waveform.csv")

plt.figure()
plt.plot(df["index"], df["input"], label="Input")
plt.plot(df["index"], df["output"], label="Output")

plt.title("Clipper Waveform")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

plt.show()
