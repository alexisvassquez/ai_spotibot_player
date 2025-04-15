# Spotibot - AI-Powered Modular Music Production Tool for Indie Artists & Creators 

---

Meet **Spotibot** - an open-source and intelligent artist-friendly music tool. Spotibot 
features AI-powered audio analysis and mood-aware music interaction.

---

Spotibot's LED light can match its colors and song or playlist suggestions to 
the user's mood through the phenomenon of mood detection. 
**Small and simple, yet technical and powerful at the same time.**

---

I update this repo continuously via my local terminal. :)

---

## Features
- Mood detection from audio files
- Spectral + MFCC-based analysis
- Integrated Spotify API for playlist input with room for future extensions
- Spotify integration: import playlists, analyze mood tracks (in development)
- LED output logic for physical interaction
- Modular codebase (using Python + C/C++)
- Built with musicians in mind

---

## License
MIT (open-source and free to use for indie artists)

---

## Project Modules
Spotibot is modular by design, allowing for rapid extension into a full-scale music AI and 
production framework. The system will be organized into the following key components:

### 1. audio/extraction.py
**Purpose:** Feature extraction from audio files
**Current Capabilities:**
- Mel-frequency cepstal coefficients (MFCC)
- Spectral contrast
- Tempo + beat tracking
**Future Expansion:**
- Key detection
- Genre classification
- Dynamic range + loudness modeling

---

### 2. audio/mood_classifier.py
**Purpose:** Analyze extracted features and assign mood tags
**Current Capabilities:**
- Basic SVM model trained on open-label audio sets
- Custom mood categories: happy, calm, energetic, sad, relaxed, angry
**Future Expansion:**
- Neural network mood embedding
- Mood-to-mixtrack recommendation
- Personalized training datasets

---

### 3. audio/audio-utils.cpp + audio_utils.h + pulseaudio_oss.sh + led_response.cpp
**Purpose:** Real-time audio playback + mood-responsive LED control
**Current Capabilities:**
- C++ PortAudio-based playback 
- Shell script to manage audio routing for PortAudio
- GPIO/LED trigger on classification results
**Future Expansion:**
- Reactive visual patterns
- BPM-sync lighting
- Live mode for DJ controller input

---

### 4. interface/bot_response.py + pcvoice.mp3
**Purpose:** Spotibot personality/voice layer for interactivity
**Current Capabilities:**
- Early logic for vocalized responses to user mood/input
- Default TTS voice or interaction prompt
**Future Expansion:**
- Integration with a personality engine

---

### 5. datasets/
**Purpose:** Audio files, metadata, and ML training targets
**Current Format:**
- Metadata syncing with Spotify API
- Manual labeling for mood, BPM, genre
**Future Expansion:**
- JSON + CSV per track
- Open contributor mood tag dataset
- Dataset visualizer UI

---

## System Map (Coming Soon)
I will publish a full architectural diagram of how Spotibot's components connect across 
Python + C++ + frontend.
**Spotibot will rave. Thank you :)**

---

### Requirements
- Python 3.10+
- CMake 3.18+
- librosa, scikitlearn, sounddevice (please refer to requirements.txt)
- PortAudio or PulseAudio

---

## Getting Started
```bash
git clone https://github.com/alexisvassquez/ai_spotibot_player.git
cd ai_spotibot_player
pip install -r requirements.txt
mkdir build && cd build
cmake ..
make
