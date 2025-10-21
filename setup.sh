#!/usr/bin/env bash

# AudioMIX / Juniper2.0 Setup Script (Lite)
# For contributors or systems with dependencies already installed

echo "🎛️  Preparing AudioMIX Python environment (amenv)..."
sleep 1

# Step 1: Create Python AudioMIX venv if missing
if [ ! -d "amenv" ]; then
    echo "🎧  Creating virtual environment: amenv/"
    python3 -m venv amenv
else
    echo "🎧  Virtual environment 'amenv' already exists."
fi

# Step 2: Activate environment
echo "⚙️  Activating environment..."
source amenv/bin/activate

# Step 3: Upgrade pip & wheel
echo "📤  Upgrading pip and wheel..."
pip install --upgrade pip wheel setuptools

# Step 4: Install project requirements
if [ -f "requirements.txt" ]; then
    echo "📦  Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found! Please make sure it's in the project root."
    exit 1
fi

# Step 5: Quick verification
echo "🔦  Checking key packages..."
python3 - <<'PY'
import torch, librosa, pandas
print("Torch:", torch.__version__)
print("Librosa:", librosa.__version__)
print("Pandas:", pandas.__version__)
PY

echo ""
echo "🎵  AudioMIX setup complete!"
echo "Activate anytime with:"
echo "  source amenv/bin/activate"
echo ""
echo "🎛️  Happy mixing! - 🌐 AMV Digital Studios"
