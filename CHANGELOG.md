# 📦 CHANGELOG

All notable changes to this project will be documented in this file.

---

## [v0.1-alpha] - 2025-04-20

### Added
- `analyze_audio.py` with MFCC, spectral contrast, and BPM analysis
- Initial `main.cpp` and `audio_utils.cpp` for C++ PortAudio integration
- `initial-script.py` prototype and CMake configuration for dual-language build
- Spotibot LED + mood mapping draft
- First public repo structure and commit

---

Future releases will include:
- AudioScript DSL for user-programmable logic
- Arduino LED integration layer
- System map + visual architecture
- Artist-facing UI and Electron/Flask-based interaction layer

---

## [v0.2-dev] - 2025-05-13

### Added
- `led/` and `led-service/` modules for mood-to-RGB control and CLI-triggerable LED response
- `main.py` in `led-service` to accept JSON input (e.g., `{ "mood": "hype", "bpm": 135 }`)
- Custom color profile mappings and animation patterns (strobe, fade, pulse)
- Mood classification output now returns a full JSON object for downstream integration
- `ETHICAL_AI_MANIFESTO.md` — AudioMIX ethical design and AI principles
- Updated `README.md` to include:
  - JSON-based mood engine
  - Live performance engine reference
  - Ethical AI section

### Changed
- Improved project language to reflect real-time modular architecture
- Replaced “small and simple” messaging with “Modular, expressive, and built for real-time creative performance.”

### Fixed
- Cleaned Git references and removed hardcoded API secrets from committed files
- Regenerated and secured Spotify API credentials; `.env` pattern recommended

---

## [v0.2-dev] - 2025-06-26

### Added
- `track_engine.py`: foundational `Track` class with volume, mute, and clip storage
- `crossfade.py`: threaded volume crossfader between tracks with real-time feedback
- AudioScript commands: `add_track()`, `add_clip()`, `set_volume()`, `mute_track()`, `crossfade()`
- ASCII VU meter output in shell reflecting real-time track volumes
- LED pulse logic tied to dominant track volume, scaled 60–200 BPM
- Juniper2.0 shell narration for transitions and system feedback (`say()`)
- Shell visual enhancements: emoji support, LED logs, mood context logs
- `pcvoice.mp3` (moved to `interface/`): original Spotibot voice now canonized as Juniper2.0's audio intro

### Changed
- Refactored shell logging to route through `say()` for consistent emoji-based output
- Updated `pulseaudio_oss.sh` for modern Crostini compatibility

### Fixed
- Git move/restore issue with legacy Spotibot files
- PulseAudio environment handling under non-owner ChromeOS user accounts

### Added
- `sampler.py`: AudioScript-based sample trigger engine with `load_sample()` and `trigger_sample()`
- Real-time LED pulse feedback when triggering samples
- Support for PCM `.wav` file playback via `aplay`
- Logging of sample playback metadata (bitrate, channels, frequency)

### Added
- `sequencer.py`: Step-based pattern engine with `define_pattern()` and `play_pattern()` commands
- AudioScript DSL support for BPM-controlled sample sequencing
- Multi-threaded playback with internal `sequence_loop()` logic
- Real-time LED pulses and PCM playback for each active step
- CLI-safe pattern parsing via `shlex` for string-encoded step sequences

### Fixed
- Casted BPM string argument to `float()` inside `play_pattern()` to prevent type errors
- Updated `parse_and_execute()` in `audioscript_runtime.py` to use `shlex.split()` for safe comma handling in string arguments

---

## [v0.2.1] - 2025-07-05

### Added
- `color(color)` AudioScript command to set static LED color
- `fade(color, duration)` command for LED fade transitions
- `delay(seconds)` command for pausing scripts
- `set_zone(zone)` command for targeting LED regions
- Persistent command history saved to `~/.audioscript_history`
- Arrow key support via `readline` for CLI shell editing

### Changed
- Refactored `shell_tools.py` to instantiate `LightController` properly
- Updated LED command feedback with zone-aware output and emojis
- Improved developer experience for AudioScript Shell CLI

### Fixed
- Resolved `ImportError` when accessing LED controller methods inside class

---

## [v0.2.2] - 2025-07-14
### Added
- Modular command loader via `load_dynamic_commands()` in `shell_tools.py`
- `fade_mod` command as proof-of-concept for dynamic CLI modules

### Fixed
- Resolved circular import issues by moving `say()` to `utils/shell_output.py`
- Normalized command parsing to pass arguments as list to `run(args)`

---

## [v0.3.0] - 2025-07-20
### Added
- Implemented `eq_dataset.py` to dynamically load features and label EQ presets from audio directory and combined JSON
- Built and debugged `plot_eq_presets.py` for visualizing EQ profiles using matplotlib, with smart parsing of both dict and list formats
- Added support for color-coded line plots, log-scaled frequency axes, and auto-saving plots to `docs/plots/`
- Integrated debug print logs and validation checks for preset data integrity
- Created `lightning_module.py` using PyTorch Lightning for training models to infer EQ presets from MFCC + spectral contrast
- Linked `presets_combined.json` as unified preset source
- Synced local environment with GCP (Google Cloud Platform), created multi-region storage bucket for AudioMIX training data
- `version.py` to keep track of version control via CLI

### Changed
- Updated plotting script to parse `gain_db` instead of `gain` field
- Reorganized project tree and confirmed compatibility with GCP CLI utilities

### Fixed
- Multiple goblins involving invalid filter structures, empty presets, and incorrect JSON parsing during plotting

---

## [0.3.1] - 2025-07-22

### Added
- 🎚️ `train_eq_model.py` script to train a Lightning PyTorch model for EQ classification
- 🧠 `LightningEQNet` model with support for multi-label output: `bass_boost`, `mids_cut`, `treble`
- 🗃️ `EQDataset` with MFCC + Spectral Contrast feature extraction via `librosa`
- ✅ `predict_eq.py` script to infer EQ tags from new `.wav` or `.mp3` files
- 💾 Saved model checkpoint at `models/eq_model.pt` and class labels in `models/eq_labels.txt`

### Notes
- First successful end-to-end ML flow: custom audio → features → model training → prediction
- EQ predictions are fully aligned with expected outputs (0.99–1.00 confidence for trained tags)
- No GPU required; model trains and runs inference entirely on CPU inside Chromebook CLI
- Began adding Spotify integration with `extract_spotify_features.py` for model training, but ran into some 403 goblins due to CA certificate mismatch on Crostini. Will need to run from GCP. 
