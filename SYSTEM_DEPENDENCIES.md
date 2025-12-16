# AudioMIX – System Dependencies

AudioMIX is a hybrid Python + native audio platform.
The following system-level dependencies must be installed
before installing Python requirements.

---

## Build Toolchain
- CMake >= 3.22
- C++17-compatible compiler
  - gcc/g++ (Linux)
  - clang (macOS)
  - MSVC (Windows)

---

## Audio Stack
- PortAudio (required)
- ALSA (Linux)
- PulseAudio or PipeWire (recommended on Linux)

---

## MIDI Support
- System MIDI backend (ALSA MIDI / CoreMIDI / Windows MIDI)

---

## Python
- Python >= 3.11
- pip
- python3-venv (Debian/Ubuntu)

---

## Notes
Many Python audio packages (PyAudio, sounddevice, pyalsaaudio)
are thin bindings over system libraries. If these system
dependencies are missing, pip installation may succeed
but runtime audio I/O will fail.
