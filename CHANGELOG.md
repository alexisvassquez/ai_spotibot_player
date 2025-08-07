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
- `train_eq_model.py` script to train a Lightning PyTorch model for EQ classification
- `LightningEQNet` model with support for multi-label output: `bass_boost`, `mids_cut`, `treble`
- `EQDataset` with MFCC + Spectral Contrast feature extraction via `librosa`
- `predict_eq.py` script to infer EQ tags from new `.wav` or `.mp3` files
- Saved model checkpoint at `models/eq_model.pt` and class labels in `models/eq_labels.txt`

### Notes
- First successful end-to-end ML flow: custom audio → features → model training → prediction
- EQ predictions are fully aligned with expected outputs (0.99–1.00 confidence for trained tags)
- No GPU required; model trains and runs inference entirely on CPU inside Chromebook CLI
- Began adding Spotify integration with `extract_spotify_features.py` for model training, but ran into some 403 goblins due to CA certificate mismatch on Crostini. Will need to run from GCP. 

---

## [0.3.1] – 2025-07-23
### Added
- New `Ethical API Use` section in README.md outlining responsible, non-scraping interaction with the Spotify Web API.
- Added working `spotify/diagnostic.py` test script for initial Spotify API integration.

### Changed
- Renamed `extract_spotify_features.py` to `spotify_api_features.py` for clarity and better alignment with project goals.

### Notes
- This update reinforces the project's commitment to API transparency, ethical data use, and support for artist integrity.

---

## [0.3.1] - 2025-07-27
### Added
- `train_eq_model.py`: Complete EQ model training pipeline using precomputed audio features and EQ label annotations.
- `flatten_features()` method to dynamically flatten all relevant audio feature structures.
- Debug logging for label/feature key matching, sample count, and input shape diagnostics.

### Fixed
- Feature-label mismatch errors due to structural assumptions.
- AttributeError caused by missing `flatten_features()` method in `EQDataset`.
- Deprecation warnings and formatting issues in `analyze_audio.py` related to `tempo` parsing.
- Overwriting issue in `audio_features.json` — now supports append-and-merge logic for multiple sample feature entries.

### Notes
- EQ model now successfully loads features from `audio/analysis_output/data/audio_features.json` and labels from `eq_labels.json`.
- Current state: **Model training confirmed working. Still in test mode.**

---

## [0.3.2] - 2025-08-02
### Added
- **PyTorch EQ Model Inference**:
  - Implemented `predict_eq.py` to load `eq_model.pt` and extract features.
  - Predicted multi-label EQ tags with confidence scores from `.wav` and `.mp3` files.
  - Added CLI support for individual file prediction.

- **Auto-EQ Application Pipeline**:
  - Enhanced `predict_and_apply_eq.py` to apply predicted EQ presets to input files.
  - Integrated dynamic preset loading with fallback warnings for unknown tags.
  - Generated matching `.audioscript` files for downstream AudioScript processing.

- **New Presets for Bass Enthusiasts**:
  - Added `"bass_plus"` and `"super_bass"` EQ profiles for enhanced low-end emphasis.
  - Improved label detection to match model output with available presets.

- **Waveform JSON Export Tool**:
  - Introduced `waveform_to_json.py` in `dev_tools/`.
  - Downsamples audio waveforms to 1000-point JSON arrays.
  - Supports waveform duration, samplerate, and amplitude-normalized points.
  - Includes `--markers` CLI flag for custom loop timestamps (e.g., `--markers "intro=0,drop=25"`).

- **Audio Format Auto-Conversion**:
  - Auto-converts `.mp3`, `.m4a`, and `.aac` to `.wav` using `pydub` + `ffmpeg`.
  - Ensures consistent waveform output and compatibility with `soundfile`.

### Fixed
- Fixed `ModuleNotFoundError` for `predict_eq.py` by using `-m` execution (`python3 -m audio.ai.modules.predict_eq`).
- Resolved `NameError` and `TypeError` in `waveform_to_json.py` caused by variable mismatches and data type goblins (e.g., list vs dict).

### Misc
- Added `dev_tools/` directory for safe, shell-free developer utilities.
- Laid groundwork for future MIDI parsing and live waveform visualization in AudioScript shell.

---

## [v0.3.3-dev] – 2025-08-06
### Added
- MIDI Feature Extraction Module (`extract_midi_features.py`)
- Genre Tag Classifier (`midi_tag_classifier.py`) with refined tag logic
- Tag-to-Behavior Mapper (`tag_to_settings.py`) with EQ and lighting scene automation
- Integrated EQ preset logic via `eq_preset()` call in `eq_commands.py`
- Created tag-based lighting and mood map (`tag_map.json`) with artistic preset names
- Began tagging system that informs Juniper2.0 performance behavior and AudioScript logic

### Updated
- Expanded tag support to include `modern_pop`, `electronic_dance`, and `classical_expressive`
- Confirmed system prints intelligent, stylized CLI output for user-facing feedback

### Notes
- Emotional + creative states now reflected in automated system response

