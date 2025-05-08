MOOD_COLOR_MAP = {
    "melancholy": (30, 60, 90), # Cool blue
    "hype": (255, 20, 20), # Intense red
    "chill": (0, 255, 180), # Aqua
    "reflective": (200, 160, 255), # Lilac
    "confident": (255, 215, 0),    # Gold
    "angry": (213, 0, 0), # Deep red
    "peaceful": (0, 255, 127), # Spring green
    "happy": (255, 223, 0), # Yellow
    "calm": (171, 71, 188), # Purple
    "energetic": (255, 109, 0), # Orange
    "sad": (41, 98, 255), # Blue
    "relaxed": (0, 255, 128) # Green
}

MOOD_PATTERN_MAP = {
    "happy": "blink",
    "calm": "wave",
    "energetic": "chase",
    "sad": "fade",
    "relaxed": "sparkle",
    "angry": "strobe",
    "melancholy": "fade",
    "hype": "strobe",
    "chill": "wave",
    "reflective": "glow",
    "confident": "blink",
    "peaceful": "breathe"
}

def get_color_for_mood(mood):
    return MOOD_COLOR_MAP.get(mood.lower(), (255, 255, 255)) # Default to white

def get_pattern_for_mood(mood):
    return MOOD_PATTERN_MAP.get(mood.lower(), "steady")
