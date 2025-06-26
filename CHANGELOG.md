# 📦 CHANGELOG

All notable changes to this project will be documented in this file.

---

## [v0.2-dev] - 2024-05-13

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

## [v0.1-alpha] - 2024-04-20

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

## [v0.3-dev] - 2025-06-26

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
