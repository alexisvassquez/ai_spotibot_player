import numpy as np
import scipy.signal as signal

# === Configuration ===
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

# Stores semantic EQ values (in dB)
eq_settings = {band: 0.0 for band in DEFAULT_BANDS}

# Stores active filter list from preset
active_filter_chain = []

# "semantic" or "filter"
eq_mode = "semantic"


# === Core EQ Logic ===

def apply_eq(audio_chunk, sample_rate):
    global eq_mode
    processed = np.copy(audio_chunk)

    if eq_mode == "filter":  # Uses explicit filters from a preset
        for f in active_filter_chain:
            freq = f["freq"]
            q = f["q"]
            gain_db = f["gain_db"]

            gain = 10 ** (gain_db / 20)
            b, a = signal.iirpeak(freq / (0.5 * sample_rate), q)
            b *= gain
            filtered = signal.lfilter(b, a, processed)
            processed += filtered

    elif eqmode == "semantic": # Uses semantic EQ bands (eq_settings)
        for band, freq in DEFAULT_BANDS.items():
            gain = eq_settings.get(band, 0.0)
            if gain != 0.0:
                b, a = signal.iirpeak(freq / (0.5 * sample_rate), Q=1)
                filtered = signal.lfilter(b, a, processed)
                processed += gain * filtered

    return processed


# === Mode Switching ===

def set_eq_mode(mode):
    global eq_mode
    if mode not in ["semantic", "filter"]:
        raise ValueError("Invalid EQ mode. Use 'semantic' or 'filter'.")
    eq_mode = mode

def get_eq_mode():
    return eq_mode

# === Sematic EQ Functions ===

def set_band(band_name, gain_db):
    if band_name in eq_settings:
        eq_settings[band_name] = gain_db
        set_eq_mode("semantic")

def reset_eq():
    for band in eq_settings:
        eq_settings[band] = 0.0
    set_eq_mode("semantic")

def get_status():
    return dict(eq_settings)


# === Filter Preset Loader ===

def load_preset(filters):
    global active_filter_chain
    active_filter_chain = filters
    set_eq_mode("filter")

def get_active_filters():
    return list(active_filter_chain)

def save_preset():
    return dict(eq_settings)
