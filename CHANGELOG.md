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
