from controller import LightController
from color_profiles import get_color_for_mood, get_pattern_for_mood

def react_to_audio(mood, bpm):
    led = LightController()
    color = get_color_for_mood(mood)
    pattern = get_pattern_for_mood(mood)

    if pattern == "strobe" or bpm > 140:
        led.strobe(color, bpm)
    elif pattern == "chase" or bpm > 100:
        led.pulse(color, bpm)
    else:
        led.fade_to(color, duration=2.0)

    return color
