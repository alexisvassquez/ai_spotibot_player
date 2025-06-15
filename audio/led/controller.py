class LightController:
    def __init__(self):
        self.zones = {} # { zone_name: current_color }

    def set_color(self, rgb, zone="main"):
        self.zones[zone] = rgb
        print (f"[LED:{zone}] Set color to RGB {rgb}")

    def pulse(self, rgb, bpm, zone="main"):
        self.set_color(rgb, zone)
        print (f"[LED:{zone}] Pulsing at {bpm} BPM with color {rgb}")

    def fade_to(self, rgb, duration, zone="main"):
        print (f"[LED:{zone}] Fading to {rgb} over {duration}s")
        self.zones[zone] = rgb

    def strobe(self, rgb, bpm, zone="main"):
        print (f"[LED:{zone}] Strobing {rgb} at {bpm} BPM")

    def apply_mood(self, mood, color, pattern, zone="main", bpm=120, duration=2)
        if pattern == "pulse":
            self.pulse(color, bpm, zone)
        elif pattern == "fade":
            self.fade_to(color, duration, zone)
        elif pattern == "strobe":
            self.strobe(color, bpm, zone)
        elif pattern == "wave":
            print (f"[LED:{zone}] Waving: {color} across strip")
        elif pattern == "blink":
            print (f"[LED:{zone}] Blinking {color} in intervals")
        elif pattern == "chase":
            print (f"[LED:{zone}] Chasing {color} along strip")
        elif pattern == "glow":
            print (f"[LED:{zone}] Soft glowing {color}")
        elif pattern == "sparkle":
            print (f"[LED:{zone}] Sparkling {color}")
        elif pattern == "breathe":
            print (f"[LED:{zone}] Breathing {color}")
        else:
            self.set_color(color, zone)
