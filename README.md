# AudioMIX / Spotibot - AI-Powered Modular Music Production Tool for Independent Artists & Creators 

---

Meet **AudioMIX** and its first test use case, **Spotibot** - an open-source and intelligent artist-friendly music tool. AudioMIX features AI-powered audio analysis and mood-aware music interaction.

---

AudioMIX's LED light can match its colors and song or playlist suggestions to the user's mood through the phenomenon of mood detection. 
**Modular, expressive, and built for real-time creative performance.**

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
- **Live performance engine** for real-time interaction and show control (in development)
- **CLI-parseable JSON output** for mood + BPM classification
- Built with musicians in mind

---

## Ethical AI
AudioMIX follows an open-source, emotionally-aware, and artist-first development philosophy.  
See [ETHICAL_AI_MANIFESTO.md](./ETHICAL_AI_MANIFESTO.md) for our creative mission and guiding principles.

---

## License
GNU General Public License v3 (open-source and free to use for indie artists, please refer to LICENSE.txt)

---

## Project Modules
AudioMIX is modular by design, allowing for rapid extension into a full-scale music AI and production framework. The system will be organized into the following key components:

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

### 3. audio/main.cpp + audio_utils.h + pulseaudio_oss.sh + led_response.cpp
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
- JSON parsing logic per track
**Future Expansion:**
- CSV per track
- Open contributor mood tag dataset
- Dataset visualizer UI

---

### 6. led-service/
**Purpose:** LED control microservice for live color pattern output based on mood/BPM JSON input  
**Current Capabilities:**
- CLI-parseable JSON endpoint (e.g. `python main.py '{"mood": "hype", "bpm": 135}'`)
- Pattern selection (strobe, pulse, fade)
- Mood → RGB mapping with custom color profiles  
**Future Expansion:**
- Socket-based live trigger events
- DMX lighting integration for venue-scale output

---

## System Map (Coming Soon)
I will publish a full architectural diagram of how AudioMIX + Spotibot's components connect across Python + C++ + frontend.
**AudioMIX will rave. Thank you :)**

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
```
