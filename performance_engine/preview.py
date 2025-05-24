import json
import time
import sys

def simulate_led_output(color, pattern, duration=1000):
    r, g, b = color
    print ("\n[PREVIEW] Simulated LED Output")
    print ("----------------------------")
    print (f"Color: RGB({r}, {g}, {b})")
    print (f"Pattern: {pattern}")
    print (f"Fade Duration: {duration}ms")
    print ("----------------------------\n")
    time.sleep(duration / 1000)

def preview_from_json(json_input):
    try:
	data = json.loads(json_input)
	mood = data.get("mood", "unknown")
	bpm = data.get("bpm", 120)
	intensity = data.get("intensity", 100)
	fade_duration = data.get("fade_duration", 1000)

        # Import shared color map and pattern map
	from color_profiles import mood_color_map, mood_pattern_map

	base_color = mood_color_map.get(mood, (255, 255, 255)) # Defaults to white
	scaled_color = tuple(int(c * intensity / 100) for c in base_color)
	pattern = mood_pattern_map.get(mood, 'pulse')

	simulate_led_output(scaled_color, pattern, fade_duration)

	if "zones" in data:
	    print ("[INFO] Zone-specific output:")
	    for zone_id, zone_cfg in data["zones"].items():
	        z_color = tuple(zone_cfg.get("color", [255, 255, 255])) # Defaults to white
		z_pattern = zone_cfg.get("pattern", 'pulse')
		print (f" - Zone {zone_id}: RGB{z_color} / Pattern: {z_pattern}")

except json.JSONDecodeError:
    print ("[ERROR] Invalid JSON input.")
except Exception as e:
    print (f"[ERROR] {e}")

__name__ == "__main__":
print ("[PREVIEW TOOL] Paste or pipe in your JSON payload (CTRL+D to run):\n")
input_data = sys.stdin.read()
preview_from_json(input_data)
