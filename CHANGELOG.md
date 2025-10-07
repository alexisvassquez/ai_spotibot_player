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

---

## [v0.4-dev] - 2025-09-18
Includes backlog of changes previously unaccounted for.
### Added
- `__init__.py` files in `audio_providers/` and `audio_providers/bandcamp/` to treat directories as Python packages and enable clean imports.
- **Lossless/lossy playback A/B** 
  - Introduced a runtime playback mode toggle to audition “studio (lossless)” vs “real-world (lossy)” sound.
  - New AudioScript commands: `set_mode("lossless" | "lossy", codec="mp3_128" | "mp3_320" | "aac_256" | "ogg_320" | "opus_160" | "wav" | "flac")` and `get_mode()`.
  - Codec simulation implemented with ffmpeg encode -> decode round-trip to float32 WAV (48 kHz), mirroring actual streaming playback.
- **Codec helpers:** Added `audio/utils/codec_sim.py` with:
  - `roundtrip_lossy()` for encode/decode
- Extended converter to normalize any input (WAV/AIFF/FLAC/MP3/AAC/OGG/OPUS) to stereo, 48 kHz, float32 WAV for consistent analysis/playback.
- Looping support to `clip_launcher.py` for EDM/beat-making workflows.
- Expanded **Sampler** module:
  - Sampler bank loading with aliases + attribution (Freesound CC-BY, etc.)
  - Playback of samples via `sampler.play`
  - Console/show credits export for attribution.
- MIDI integration improvements:
  - `midi.py` — quantized real-time MIDI listener with `midi_map`, `midi_tick`, and clock handling.
  - `midi_bridge.py` — mapping JSON loader and tag-classification pipeline to AudioScript actions.

### Changed
- Renamed `spotify/` directory to `audio_providers/` to support Spotify and Bandcamp integrations.
- Cleaned absolute imports and typos across `sampler.py`, `midi.py`, and `midi_bridge.py`.

### Fixed
- Safer temp-file lifecycle around transcoding and simulation artifacts
- Cleanup after playback.
- Clearer errors when `ffmpeg` is not found (actionable message instead of silent failure).

### Debugging / Refactor
- Began major debugging phase of the **AudioScript Runtime** (`audioscript_runtime.py`):
  - Fixed relative import errors across multiple modules.
  - Added `register_command()` helper to cleanly register runtime commands.
  - Corrected `command_registry("...")` misuse -> proper registration calls.
  - Updated command parser to unpack arguments correctly with `*parts`.
  - Fixed variable typos (e.g., `wav_pth` -> `wav_path`) in playback function.
- Refactored **Clip Launcher** (`clip_launcher.py`):
  - Removed `sounddevice` dependency (To keep Chrom-E safe).
  - Implemented `aplay`-based fallback for audio playback.
  - Fixed retrigger logic, choke group handling, and typo bugs (`_PLAYERS[name] - pl` → `_PLAYERS[name] = pl`).
- Cleaned up **provider API** (`provider_api.py`):
  - Converted abstract method stubs to `...` to avoid indentation errors.
  - Fixed registry reference typo (`registry` -> `_registry`).
- Began auditing runtime imports for excessive top-level weight:
  - Identified heavy AI/audio imports (librosa, transformers, etc.) as a likely source of `Killed` errors on low-memory systems.
  - Planned lazy-import strategy and safe-mode module loading.
- Updated `requirements.txt`:
  - Removed `sounddevice`.
  - Marked other heavy libs as candidates for optional/deferred use.

### TODO:
- **AS Shell stability:** remove any unnecessary imports at the top-level and spread them out to fix what's causing crashes.

---

## [v0.4-dev] - 2025-09-24
### Debugging Milestone
- Completed module-by-module registration test with **Ultra-Safe Runtime**:
  - All modules imported cleanly.
  - No runtime kills when loaded individually.
  - Confirmed that `context.py` and `shared.py` are utility-only (no commands).
  - `fade_mod.py` flagged for a future `register()` implementation or conversion to helper-only.
- Verified that **runtime crashes are caused by system memory limits (Chrom-E/Crostini OOM)**, not by logic errors in the AudioScript runtime or modules.
- Introduced **safe mode strategy** (`AUDIOMIX_SAFE=1`) and allowlist-based loading for stability on resource-constrained systems.
- Reassured that overall **project architecture is sound**; AudioMIX shell and modules behave as designed once loaded.

### Notes
- *Chrom-E,* the stalwart Chromebook dev machine, successfully carried both **AudioMIX** and **Track That Money** through this stage of development. 🖤👑  
- **All hail Chrom-E, King of the Chromebooks!** 👑 Long may he reign until his teammate mini-PC arrives.  
- Future work: acquire a dedicated mini-PC teammate for heavier compilation and ML workloads, while Chrom-E continues to serve as a reliable dev/test environment.

---

## [v0.4-dev] - 2025-10-06
### Performance Engine Note
- Added `audience_listener.py` script (live mic input module)
- Detects crowd energy, cheering, or silence based on amplitude thresholds
- Used to influence `mood` and trigger LED zone changes via `trigger_zones()`
- Forms part of the Juniper2.0 reactive loop for stage-aware performances

### Added
- **Functional language features to AudioScript v0.2**:
- `let` expressions for pattern variables and FX chains
- `repeat()`, `take()`, and lazy evaluation for infinite sequences
- `with` operator for chaining FX: `play("beat") with stutter + reverb`
- `dsl_helpers.py` for Haskell-inspired functional utilities
- `runtime_state.py` to track variables, macros, and event hooks
- New `core.py` refactor of the interpreter shell
- CLI-compatible REPL with support for script evaluation and mood-aware shell
- New keywords added to `AudioScript.ebnf` grammar
- Functional-reactive design principles aligned with AudioMIX architecture
- `intro_showcase.audioscript`: official v0.2 demo script showcasing `let`, `repeat()`, `with` chaining, LED FX, and mood triggers

### Changed
- `audioscript_runtime.py` split and refactored into modular runtime components
- AudioScript README updated with new language features and functional DSL architecture
- `AUDIOSCRIPT_SPEC.md` rewritten to document lazy evaluation, chaining, and reactivity


### Fixed
- Improved REPL handling for nested command input and invalid function chains
- Robust fallback in `parse_and_execute` for misused commands
- Emoji-safe REPL output and better formatting of chained outputs
