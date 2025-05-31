import numpy as np
import scipy.signal as signal

# Default EQ bands (frequencies in Hz for 10-band system)
DEFAULT_BANDS = {
    "sub_bass": 60,
    "bass": 120,
    "low_mid": 250,
    "mid": 500,
    "high_mid": 1000,
    "presence": 2000,
    "brilliance": 4000,
    "air": 8000,
    "sparkle": 12000,
    "ultra": 16000
}

# Gain levels in dB
eq_settings = {band: 0.0 for band in DEFAULT_BANDS}

def apply_eq(audio_chunk, sample_rate, gains=None):
    """
    Apply EQ to a given audio chunk using band filters.
    """
    if gains is None:
        gains = eq_settings

    processed = np.copy(audio_chunk)
    for band, freq in DEFAULT_BANDS.items():
        gain = gains.get(band, 0.0)
        if gain != 0.0:
            # Simple peaking filter example
            b, a = signal.iirpeak(freq / (0.5 * sample_rate), Q=1)
            filtered = signal.lfilter(b, a, processed)
            processed += gain * filtered
    return

def set_band(band_name, gain_db):
    if band_name in eq_settings:
        eq_settings[band_name] = gain_db

def reset_eq():
    for band in eq_settings:
        eq_settings[band] = 0.0

def get_status():
    return dict(eq_settings)

def load_preset(preset_dict):
    eq_settings.update(preset_dict)

def save_preset():
    return dict(eq_settings)
