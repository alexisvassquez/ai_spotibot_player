from audio.audio_reactive import react_to_audio
from audio.led.controller import LightController

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

# Main function
def apply_dynamic_zoning(emotion_tags, bpm=120, debug=False)
    controller = LightController()

    for mood in emotion_tags:
        zone = EMOTION_ZONE_MAP.get(mood, get_zone_by_bpm(bpm))
        if debug:
            print (f"[Juniper2.0] Applying mood '{mood}' to zone '{zone}' at {bpm} BPM")
        react_to_audio(mood, bpm, zone)
