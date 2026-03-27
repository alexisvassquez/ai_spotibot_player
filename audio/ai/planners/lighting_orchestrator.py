import json
from audio.led.audio_reactive import react_to_audio
from audio.led.controller import LightController
from audio.ai.modules.tempo_analysis import get_bpm_from_audio

# Emotion-to-zone mapping
EMOTION_ZONE_MAP = {
    "excited": "front_strip",
    "calm": "ceiling",
    "melancholy": "back_wall",
    "intense": "floor",
    "reflective": "side_panels",
    "happy": "centerpiece",
    "angry": "strobe_beam",
    "chill": "ambient_sides",
    "confident": "main_wall"
}

# Fallback logic: assign by BPM
def get_zone_by_bpm(bpm):
    if bpm > 140:
        return "front_strip"
    elif bpm > 120:
        return "main_wall"
    elif bpm > 100:
        return "ambient_sides"
    else:
        return "top_ceiling"

wav_path = features.get("source_path") # to be passed manually
bpm = get_bpm_from_audio(wav_path)

# Main function
def apply_dynamic_zoning(emotion_tags, bpm=120, debug=False):
    controller = LightController()

    for mood in emotion_tags:
        zone = EMOTION_ZONE_MAP.get(mood, get_zone_by_bpm(bpm))
        if debug:
            print (f"[Juniper2.0] Applying mood '{mood}' to zone '{zone}' at {bpm} BPM")
        react_to_audio(mood, bpm, zone)

def load_features(path="audio/analysis_output/features_summary.json"):
    with open(path, "r") as f:
        return json.load(f)

def run_lighting_orchestration():
    data = load_features()
    bpm = int(data.get("tempo", [120])[0])
    emotion_tags = []

    # TEMP: Manually define emotion for test
    if bpm > 140:
        emotion_tags.append("intense")
    elif bpm > 120:
        emotion_tags.append("excited")
    else:
        emotion_tags.append("calm")

    apply_dynamic_zoning(emotion_tags, bpm)

if __name__ == "__main__":
    run_lighting_orchestration()
