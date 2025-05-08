class LightController:
    def __init__(self):
        self.current_color = (0, 0, 0)

    def set_color(self, rgb):
        self.current_color = rgb
        print (f"[LED] Set color to RGB {rgb}")

    def pulse(self, rgb, bpm):
        self.set_color(rgb)
        print (f"[LED] Pulsing at {bpm} BPM with color {rgb}")

    def fade_to(self, rgb, duration):
        print (f"[LED] Fading to {rgb} over {duration}s")
        self.current_color = rgb

    def strobe(self, rgb, bpm):
        print (f"[LED] Strobing {rgb} at {bpm} BPM")
