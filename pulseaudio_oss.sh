#!/bin/bash

# Start PulseAudio with proper socket location
pulseaudio --start --exit-idle-time=-1

# Export environment variable to force sound routing
export SDL_AUDIODRIVER=alsa
export AUDIODEV=hw:0,0

export PYTHON_SOUNDCARD_BACKEND=alsa

echo "PulseAudio initialized with ALSA fallback."
