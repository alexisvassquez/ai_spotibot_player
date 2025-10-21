# 🎧 AudioMIX Contributor Dataset Guide
*A community-grown dataset for the evolution of Juniper 2.0.*

---

## 💡 Purpose
AudioMIX and its AI core **Juniper2.0** learn from real creative data — not harvested or scraped,
but **contributed intentionally** by artists, engineers, and tinkerers.

This guide explains how you can safely and ethically add data that helps
Juniper 2.0 become smarter, more expressive, and more artist-aware.

---

## 🧱 What You Can Contribute

| Type | Examples | File Location |
|------|-----------|---------------|
| **Audio clips** | 10-30 s WAV/MP3 stems, loops, samples you created or own | `audio/ai/datasets/clips/` |
| **Metadata** | `AudioMIX_metadata.csv` (see schema below) | `audio/ai/datasets/AudioMIX_metadata.csv` |
| **Mood & Scene labels** | `labels.jsonl` entries for each file | `audio/ai/datasets/labels.jsonl` |
| **Feature sets** | Pre-extracted MFCC/spectral/chroma `.npz` files | `audio/ai/datasets/features/` |
| **Crowd energy traces** *(optional)* | JSONL or CSV logs from live shows (`timestamp,energy,events`) | `audio/ai/datasets/crowd/` |

---

## 📄 Metadata Schema (`AudioMIX_metadata.csv`)
**Example:**

| Column | Example | Description |
|--------|----------|-------------|
| `file` | `cvltiv8r_clean.wav` | Audio file name (relative to `clips/`) |
| `bpm` | `128` | Tempo in beats-per-minute |
| `key` | `Amin` | Musical key |
| `genre` | `hyperpop` | Broad style or mood |
| `source` | `lexy_studio` | Who created / provided the clip |
| `split` | `train` | Dataset split: `train`, `val`, or `test` |
| `energy` | `0.82` | Perceived intensity or loudness of track (0-1) Higher = more energetic, lower = mellow. Roughly est via RMS or own judgment |
| `valence` | `0.64` | Emotional positivity (0-1) 0 = dark/sad, 1 = bright/joy |
| `danceability` | `0.73` | How rhythmically "movable" track feels (0-1) |
| `reference_only` | `bool` | Mark `True` if this row is a metadata ref (e.g., Spotify stats/synthetic data). Otherwise `False` |

---

## 💬 Label Format (`labels.jsonl`)

Each line = one JSON object:

```json
{"file": "cvltiv8r_clean.wav",
 "moods": ["hype","uplifted"],
 "energy": 0.82,
 "valence": 0.61,
 "led_profile": {"pattern": "strobe", "color": "neon_cyan", "intensity": 0.7}}
```
---

## ⚖️  Licensing & Ethics
- ✅ You must own the rights to any audio you contribute.
- ✅ All data is released under Creative Commons BY 4.0 unless otherwise stated.
- ✅ No copyrighted commercial tracks (unless you own them).
- ✅ Contributions follow the spirit of the `ETHICAL_AI_MANIFESTO.md`
- 🚫 Do not include personally identifiable or private recordings.

---

## 🧭 Contribution Flow
1. Fork the repo and create a branch dataset/<yourname>.
2. Add your clips + metadata + labels.
3. Run `python3 validate_dataset.py` to check schema. (in development)
4. Commit & push:
```bash
git add audio/ai/datasets
git commit -m "Add mood-labeled clips by <yourname>"
git push origin dataset/<yourname>
```
5. Open a Pull Request describing your contribution

---

## 💡 Notes for Contributors
- Always ensure filenames in `AudioMIX_metadata.csv` match actual files in `clips/`.
- If you’re unsure of BPM or key, it’s okay to approximate — Juniper2.0 can infer and smooth values during training.
- All numeric values (`bpm`, `energy`, `valence`, `danceability`) should be real numbers, not text.
- Leave `reference_only` as `True` for template or calibration entries.

---

## 💌 Credits
Every approved contributor will be listed in a new document titled
`CONTRIBUTORS.md` under “Dataset Architects.”
You’re helping shape the emotional intelligence of **AudioMIX.**

---
> "Thank you for helping build the future of AI-assisted music production" - 🌐 AMV Digital Studios
