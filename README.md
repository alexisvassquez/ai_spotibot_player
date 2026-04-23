
# 🎧  AudioMIX - AI-Assisted Music Production & Live Performance Software

![License](https://img.shields.io/badge/license-GPLv3-blue)
![Stack](https://img.shields.io/badge/stack-Python%20%7C%20C%2B%2B%20%7C%20CMake%20%7C%20AudioScript-purple)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)
![Status](https://img.shields.io/badge/status-active%20development-brightgreen)
![AI](https://img.shields.io/badge/AI-powered-orange)
![DSP](https://img.shields.io/badge/audio-DSP-critical)
![Built For](https://img.shields.io/badge/built%20for-artists%20%26%20developers-ff69b4)

> **AudioMIX is where music production meets live performance engineering.**  
> Write a script. Make a beat. Light up a room. All from one platform.

**AudioMIX** is an open-source, AI-assisted digital audio workstation built for independent artists, producers, and developer-musicians who want more than a traditional DAW. It combines a real-time C++ DSP engine, an AI creative assistant (Juniper2.0), and ***AudioScript*** — a custom musical programming language — into a single unified system designed for both the studio and the stage.

Whether you're producing a track, coding a live set, or synchronizing LED lighting to a crowd's energy in real time, **AudioMIX** gives you the tools to do it expressively and programmatically.

> This is not just a DAW. It's a creative operating system for performers.

✨ If AudioMIX resonates, consider starring the repo and sharing it with your network.

---

## Why AudioMIX?

Most DAWs are built for the studio. Most live coding tools aren't built for artists.
**AudioMIX** bridges that gap — giving musicians the power of code without losing the feeling of performance.

- 🎛️ **Producer?** Use the DSP engine and AI mood analysis to build and refine your sound
- 🎤 **Live performer?** Script your entire show — audio, lighting, and transitions — in AudioScript
- 💻 **Developer-musician?** Extend the platform, contribute to AudioScript, or plug in your own modules

---

## AudioMIX Core Features

- Real-time DSP audio engine in C++
- AudioScript (custom musical programming DSL) for live coding features
- Mood detection from audio files with ML-based tagging
- Spectral, MFCC, beat tracking, and tempo analysis
- Integrated Spotify API for playlist input with room for future extensions
- LED output logic for physical interaction
- **Live performance engine** for visual show control
- **Audience listener** to hype up live performances based on audience input
- **AudioScript Shell** for live coding features
- **CLI-parseable JSON output** for mood + BPM classification
- Provides a foundation for AI-assisted music production

---

## Ethical AI

**AudioMIX** follows an open-source, emotionally-aware, and artist-first development philosophy.  
See [ETHICAL_AI_MANIFESTO.md](./ETHICAL_AI_MANIFESTO.md) for our creative mission and guiding principles.

---

## License

GNU General Public License v3 (open-source and free to use for independent artists and developers, please refer to [LICENSE.txt](./LICENSE.txt))

---

## Project Modules

**AudioMIX** is modular by design, allowing for rapid extension into a full-scale music AI and production framework. The system will be organized into the following key components:

### 1. `audio/dsp` and `audio/ai`

**Purpose:** real-time DSP audio engine and feature extraction from audio files using AI/ML models for mood and BPM classification.
**Current Capabilities:**

- Mel-frequency cepstral coefficients (MFCC)
- Spectral contrast
- Tempo + beat tracking
- Dynamic range + loudness modeling
**Future Expansion:**
- Key detection
- Genre classification

---

### 2. `performance-engine/`

**Purpose:** Real-time control and exection
**Current Capabilities:**

- Audience listener
- EQ settings
- MIDI player (in dev)
- AudioScript runtime shell for live coding performances
- Python modules for AI/ML
**Future Expansion:**
- Hardware capabilities

---

### 3. `led-service/`

**Purpose:** LED control microservice for live color pattern output based on mood/BPM JSON input  
**Current Capabilities:**

- CLI-parseable JSON endpoint (e.g. `python main.py '{"mood": "hype", "bpm": 135}'`)
- Pattern selection (strobe, pulse, fade)
- Mood → RGB mapping with custom color profiles  
**Future Expansion:**
- Socket-based live trigger events
- DMX lighting integration for venue-scale output

---

### 4. `audio_providers/`

**Purpose:** External integrations and ethical API Use

**No Scraping Data:**

- This project interacts with Spotify through the **official Spotify Web API**, utilizing authenticated access and approved scopes.
- No scraping is used at any point.
- All audio feature extraction is handled through permitted endpoints provided by Spotify, in accordance with their [Developer Terms of Service](https://developer.spotify.com/terms).
- This ensures ethical, transparent, and respectful use of artist and user data.
- Includes Bandcamp embed

> The purpose of these features is to support creative analysis and mood-based musical applications—not to exploit or misrepresent Spotify’s platform.

---

### 5. `datasets/`

**Purpose:** Audio files, metadata, and ML training targets
**Current Format:**

- Metadata syncing with Spotify API
- Manual labeling for mood, BPM, genre
- JSON parsing logic per track
**Future Expansion:**
- CSV per track
- Open contributor mood tag dataset
- Dataset visualizer UI

---

## AudioScript - The Language of AudioMIX

***AudioScript (AS)*** is a custom musical programming language built from the ground up for **AudioMIX.** It gives artists and developers a human-readable, expressive way to control audio playback, LED behaviors, mood transitions, and live performance scenes — all in code.

Think of it as sheet music for the digital age. Instead of clicking through menus, you write a script. AudioScript handles the rest.

---

### AudioScript (AS) Features

- Human-readable, whitespace-sensitive syntax
- Modular commands: `play()`, `glow()`, `pulse()`, `mood.set()`, and more
- CLI interpreter support with real-time execution
- Designed for live performance, emotional scripting, and AI augmentation
- Influences of Python, C++, and Haskell

---

### Two Branches. One Language

AudioScript is designed with two distinct execution modes, each built for a different creative context:

**🔧 IR (Intermediate Representation)**  
The machine-readable layer of AudioScript. IR is auto-generated from its own compiler and designed for precision — ideal for compiled performance pipelines, AI-assisted generation, and programmatic show control. If Juniper2.0 is writing your set, she's writing in IR.

**🎛️ Live**  
The human-facing layer. Live mode is optimized for real-time coding performances — expressive, forgiving, and designed to be written on stage. Change a mood, trigger a light pattern, drop a beat. All without stopping the show.

---

### AudioScript Features

- Human-readable, whitespace-sensitive syntax
- Modular commands: `play()`, `glow()`, `pulse()`, `mood.set()`, and more
- CLI interpreter with real-time execution
- Two execution modes: IR (machine-generated) and Live (performance-optimized)
- Influenced by Python, C++, and Haskell
- Designed for AI augmentation via Juniper2.0

### Sample Script

```python
mood.set("uplifted")
glow("lilac")
play("intro.wav")
pulse("yellow", bpm=120)
```

**AudioScript** is actively evolving alongside AudioMIX.

View the full language spec here: [AUDIOSCRIPT_SPEC.md](./AUDIOSCRIPT_SPEC.md)

Explore the `audioscript/` directory to see it in action, including the compiler, CLI interpreter, and test scripts.

---

## Juniper2.0 – The AudioMIX AI Core

Most AI tools are general purpose. Juniper2.0 is not.

Juniper2.0 is the intelligent creative assistant built specifically for AudioMIX. She understands your sound, your mood mappings, your LED configurations, and your AudioScript syntax — and she uses that context to collaborate with you in real time, not just respond to prompts.

> She is not here to replace the artist. She is here to make the artist unstoppable.

---

### What Juniper2.0 Does

**🎵 AudioScript Generation & Debugging**  
Juniper2.0 can write, suggest, and debug AudioScript in both IR and Live modes.
Describe what you want your show to feel like — she'll script it.

**🎛️ Mood-Optimized Production Assistance**  
From EQ suggestions to track flow recommendations, Juniper2.0 analyzes the emotional arc of your set and helps you shape it intentionally.

**💡 LED & Emotional Mapping**  
Tell her the mood. She'll map the light. Juniper2.0 connects your audio's emotional fingerprint to your LED configurations automatically.

**🎤 Live Performance Guidance**  
During a live set, Juniper2.0 can respond to audience energy, suggest transitions, and keep your performance moving — all in real time.
**Juniper2.0** will be integrated into the CLI and future UI to provide intelligent inline suggestions and personalized creative support for musicians and coders alike.

---

### Design Philosophy

Juniper2.0 is built on an artist-first principle: **she amplifies creative intent, she does not override it.**

Every suggestion she makes is traceable, adjustable, and ultimately in service of your vision.

> "Juniper doesn't replace the artist — she collaborates with them."

Juniper2.0 will be integrated into the CLI and the AudioMIX-Electron desktop UI, providing intelligent inline suggestions and personalized creative support whether you're in the studio, in your bedroom, or on the stage.

---

## System Architecture Map

Below is the current system-level architecture of **AudioMIX,** including modules written in *Python*, *C++,* and *AudioScript:*

![AudioMIX System Map](docs/system_map.png)

### Project Tree

A full snapshot of the current project structure can be found in [`AudioMIX_project_tree.txt`](docs/AudioMIX_project_tree.txt).

---

## 🖥️  AudioMIX-Electron — Official Desktop Interface

**AudioMIX-Electron** is the companion desktop UI for the **AudioMIX Core Engine.**
It provides a secure, dynamic, and visually reactive front-end built with Electron v39 and Node 22, designed to emulate the clean utility of VS Code while introducing DAW-style elements such as mixers, EQ panels, and LED feedback zones.

> 💡 Status: Actively in development — currently at the “First Breath” milestone (v0.1-dev).

### Repository

[AudioMIX-Electron on GitHub](https://github.com/alexisvassquez/audiomix-electron)

### AudioMIX-Electron Features

- Secure sandboxed Electron shell (context isolation, no Node exposure)
- Real-time backend heartbeat and system status bar
- Modular UI framework ready for EQ, Mixer, and LED visualization panels
- Full-screen responsive layout with universal keyboard-friendly controls
- Preload bridge for safe IPC between renderer and backend (FastAPI / C++)

| Layer           | Repository                                                               | Purpose                                                        |
| :-------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------- |
| **Core Engine** | [`AudioMIX`](https://github.com/alexisvassquez/ai_spotibot_player) | Backend DSP, AI, and system logic.                |
| **Desktop UI**  | [`AudioMIX-Electron`](https://github.com/alexisvassquez/audiomix-electron) | Visual front-end shell for artists, producers, and developers. |

Once the FastAPI bridge is live, the Electron client will automatically surface real-time system info from the AudioMIX backend.

---

## Dependencies

AudioMIX is a hybrid Python + native audio platform. It relies on both Python packages and system-level audio/build tools.

### Requirements

Python requirements are listed in `requirements.txt` and can be installed via the instructions below:

- Python 3.10+
- CMake 3.18+
- librosa, scikitlearn, sounddevice (please refer to requirements.txt)
- PortAudio or PulseAudio

### Getting Started

```bash
git clone https://github.com/alexisvassquez/ai_spotibot_player.git
cd ai_spotibot_player
pip install -r requirements.txt
mkdir build && cd build
cmake ..
make
```

### UI Preview

```bash
git clone https://github.com/alexisvassquez/audiomix-electron.git
cd audiomix-electron
npm install
npm start
```

---

© 2026  Alexis M Vasquez, Software Engineer / AMV Digital Studios
