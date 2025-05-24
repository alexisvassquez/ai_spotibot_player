import serial
import json
import time
from color_profiles import mood_color_map, mood_pattern_map

class LEDController:
    def __init__(self, port='/dev/ttyUSB0'), baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2) # Give time for Arduino to reset

    def send_color(self, rgb_tuple):
        r, g, b = rgb_tuple
        command = f"COLOR: {r},{g},{b}\n"
        self.ser.write(command.encode())
        print (f"[LED] Sent color: {command.strip()}")

    def send_pattern(self, pattern):
        command = f"PATTERN:{pattern}\n"
        self.ser.write(command.encode())
        print (f"[LED] Sent pattern: {command.strip()}")

def scale_brigtness(rgb, intensity):
    intensity = max(0, min(intensity, 100)) # Clamp between 0-100
    return tuple(int(c * intensity / 100) for c in rgb)

class MoodDetector:
    def __init__(self):
        self.mood_color_map
        self.mood_pattern_map

    def get_color(self, mood, intensity=100):
        base_color = self.color_map.get(mood, (255, 255, 255)) # Default to white
	return scale_brightness(base_color, intensity)

    def get_pattern(self, mood, bpm):
	if bpm >= 130:
	    return 'strobe'
	return self.mood_pattern_map.get(mood, 'pulse')

def handle_event(data, detector, controller):
    mood = data.get("mood")
    bpm = data.get("bpm", 120)
    intensity = data.get("intensity", 100)

    if not mood:
	print ("[WARN] Missing 'mood' in input")
	return

    rgb = detector.get_color(mood, intensity)
    pattern = detector.get_pattern(mood, bpm)

    controller.send_color(rgb)
    controller.send_pattern(pattern)

if __name__ == "__main__":
    detector = MoodDetector()
    controller = LEDController()

    print ("[INFO] Listening for mood/BPM JSON objects...")
    while True:
	try:
	    if controller.ser.in_waiting:
		line = controller.ser.readline().decode().strip()
		print (f"[INPUT] {line}")
		try:
		    data = json.loads(line)
		    handle_event(data, detector, controller)
		except json.JSONDecodeError:
		    print ("[ERROR] Invalid JSON received")
	except KeyboardInterrupt:
	    print ("\n[INFO] Stopping listener...")
	    break
