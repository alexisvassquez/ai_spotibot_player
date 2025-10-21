#!/usr/bin/env bash

# AudioMIX / Juniper2.0 Installation Script
# Modular AI Music Production Framework

echo "🎚️  Setting up AudioMIX environment..."
sleep 1

# Step 1: System updates
echo "🔧  Updating system pacakages..."
sudo apt-get update -y && sudo apt-get upgrade -y

# Step 2: Core dependencies
echo "📥  Installing system-level libraries..."
sudo apt-get install -y \
    build-essential \
    python3-dev python3-pip python3-venv \
    libasound2 libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    alsa-utils \
    git \
    curl

# Step 3: Python virtual environment (AudioMIX environment)
if [ ! -d "amenv" ]; then
    echo "🎧  Creating AudioMIX virtual environment..."
    python3 -m venv amenv
else
    echo "🎧  Virtual environment 'amenv' already exists."
fi

echo "⚙️  Activating environment..."
source amenv/bin/activate

# Step 4: Upgrade pip & wheel
pip install --upgrade pip wheel setuptools

# Step 5: Install Python requirements
echo "📦  Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found! Please make sure it exists in the project root."
    exit 1
fi

# Step 6: Verify key installs
echo "✅  Verifying installation..."
python3 - <<'PY'
import sys, torch, librosa
try:
    import sounddevice, alsaaudio
    print("Python:", sys.version)
    print("Torch:", torch.__version__)
    print("Librosa:", librosa.__version__)
    print("SoundDevice:", hasattr(sounddevice, "query_devices"))
    print("ALSA:", hasattr(alsaaudio, "PCM"))
except Exception as e:
    print("⚠️  Verification warning:", e) 
PY

# Step 7: Post-install message
echo ""
echo "🎵  AudioMIX installation complete!"
echo "To activate your environment later, run:"
echo "  source amenv/bin/activate"
echo ""
echo "You're ready to train Juniper2.0 and start performing!"
echo "🎛️  Happy mixing! - 🌐 AMV Digital Studios"
