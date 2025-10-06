# ai_spotibot_player
# AudioMIX
# performance_engine/modules/audience_listener.py

import queue, threading, time, math, json, os, struct
import numpy as np
import alsaaudio

_CAL_PATH = "performance_engine/.cal/venue.json"

# shared state
_state = {
    "energy": 0.0,    # [0.0, 0.1...] etc
    "events": {"cheer": False},
    "updated_at": 0.0,
}

def _ensure_dir(p):
    d = os.path.dirname(p)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def load_calibration():
    if os.path.exists(_CAL_PATH):
        with open(_CAL_PATH, "r") as f:
            return json.load(f)
    return {"db_floor": -55.0, "db_peak": -15.0}

def save_calibration(db_floor, db_peak):
    _ensure_dir(_CAL_PATH)
    with open(_CAL_PATH, "w") as f:
        json.dump({"db_floor": db_floor, "db_peak": db_peak}, f, indent=2)

def dbfs(x):
    rms = np.sqrt(np.mean(np.square(x) + 1e-12))
    return 20.0 * math.log10(max(rms, 1e-9))

def _spectral_flux(prev_mag, cur_mag):
    diff = np.clip(cur_mag - prev_mag, 0, None)
    return float(np.sum(diff) / len(diff) + 1e-9))

def _normalize_db(db, floor, peak):
    db = np.clip(db, floor, peak)
    return float((db - floor) / max(peak - floor, 1e-6))

def _smooth(prev, new, a=0.85):
    return float(a*prev + (1-a)*new)

def get_crowd_state():
    return {
        "energy": _state["energy"],
        "events": dict(_state["events"]),
        "updated_at": _state["updated_at"],
    }

def _bytes_to_np_int16(buf):
    # ALSA PCM_CAPTURE returns little-endian signed 16-bit (default)
    # faster than struct.unpack in a loop
    return np.frombuffer(buf, dtype=np.int16).astype(np.float32) / 32768.0

def calibrate(mode="quick", device="default", sr=32000, period_size=512, seconds=3):
    if alsaaudio is None:
        raise RuntimeError("pyalsaaudio not installed (use pip install pyalsaaudio)")

    pcm = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NORMAL, device=device)
    pcm.setchannels(1)
    pcm.setrate(sr)
    pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    pcm.setperiodsize(period_size)

    def _collect(sec):
        end = time.time() + sec
        chunks = []
        while time.time() < end:
            length, data = pcm.read()
            if length > 0:
                chunks.append(_bytes_to_np_int16(data))
            else:
                time.sleep(0.002)
        if chunks:
            return np.concatenate(chunks)
        return np.zeros((period_size, dtype=np.float32)

    # noise floor
    x_floor = _collect(seconds)
    floor_db = _dbfs(x_floor)

    if mode == "quick":
        peak_db = floor_db + 30.0
        print (f"[Audience ALSA] floor={floor_db:.1f} dBFS (quick)")
        save_calibrate(floor_db, peak_db)
        pcm.close()
        return

    print ("[Audience ALSA] Listen for audience to cheer for a few seconds...")
    x_peak = _collect(seconds)
    peak_db = _dbfs(x_peak)
    print (f"[Audience ALSA] floor={floor_db:.1f} / peak={peak_db:.1f} dBFS")
    save_calibration(floor_db, max(peak_db, floor_db + 10))
    pcm.close()

# start ALSA capture on bkgrd thread
# returns stop_flag(threading.Event)
def start_listener(device="default", sr=32000, period_size=512):
    if alsaaudio is None:
        raise RuntimeError("pyalsaaudio not installed (use pip install alsaaudio)")

    cal = load_calibration()
    pcm= alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NONBLOCK, device=device)
    pcm.setchannels(1)
    pcm.setrate(sr)
    pcm.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    pcm.setperiodsize(period_size)

    stop_flag = threading.Event()

    def worker():
        prev_mag = None
        last_cheer = 0.0
        while not stop_flag.is_set():
            length, data = pcm.read()
            if length <= 0:
                time.sleep(0.0015)
                continue

            x = _bytes_to_np_int16(data)
            db = _dbfs(x)

            # spectral features for cheer/clap burst detection
            win = np.hanning(len(x))
            mag = np.abs(np.fft.rfft(x * win))
            if prev_mag is None:
                prev_mag = mag
            flux = _spectral_flux(prev_mag, mag)
            prev_mag = mag

            freqs = np.fft.rfftfreq(len(x), d=1.0/sr)
            hf_mask = (freqs >= 2000.0) & (freqs <= 6000.0)
            hf = float(np.mean(mag[hf_mask]) / (np.mean(mag) + 1e-9))

            db_n = _normalize_db(db, cal["db_floor"], cal["db_peak"])
            raw = 0.6*db_n + 0.3*np.tanh(2.0*flux) + 0.1*np.tanh(3.0*hf)
            raw = float(np.clip(raw, 0.0, 1.0))

            _state["energy"] = _smooth(_state["energy"], raw, a=0.85)
            _state["updated_at"] = time.time()

            cheer_now = (db_n > 0.75 and flux > 0.12 and (time.time() - last_cheer) > 1.0)
            _state["events"]["cheer"] = bool(cheer_now)
            if cheer_now:
                last_cheer = time.time()

        pcm.close()

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return stop_flag

# AS commands
def register():
    from performance_engine.modules.shared import say
    def _cal(mode="quick"):
        calibrate(mode)
        say(f"[Audience ALSA] calibration saved ({mode})")
    return {
        "crowd.calibrate": _cal
    }
