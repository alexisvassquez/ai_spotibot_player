import threading
import time
from performance_engine.modules.track_engine import track_registry
from performance_engine.modules.led_controller import pulse
from performance_engine.utils.shell_output import say

def crossfade(track_a, track_b, duration=4.0):
    try:
        duration = float(duration)
        steps = 50
        step_duration = duration / steps

        trackA = track_registry.get(track_a)
        trackB = track_registry.get(track_b)

        if not trackA or not trackB:
            print(f"❌ One or both tracks not found: {track_a}, {track_b}")
            return

        # Narration from Juniper2.0
        say(f"Juniper2.0: Fading from {track_a} → {track_b}...prepare for lift off", "🎙️")

        def vu_bar(vol):
            bar_len = int(vol * 20)
            return "█" * bar_len + " " * (20 - bar_len)

        def fade():
            for i in range(steps + 1):
                t = i / steps
                trackA.volume = 1.0 - t
                trackB.volume = t

                # VU meter
                bar_a = vu_bar(trackA.volume)
                bar_b = vu_bar(trackB.volume)
                print (f"{track_a}: {bar_a} {trackA.volume:.2f} | {track_b}: {bar_b} {trackB.volume:.2f}", "🎛️")

                # LED feedback (pulse based on dominant volume)
                dominant = track_a if trackA.volume > trackB.volume else track_b
                vol = max(trackA.volume, trackB.volume)
                bpm = int(60 + vol * 140) # volume 0.0-1.0 → BPM 60-200
                pulse("blue" if dominant == track_a else "pink", bpm)
 
                time.sleep(step_duration)

            say (f"🔁 Crossfade complete: {track_a} → {track_b}", "💥")

        threading.Thread(target=fade).start()

    except Exception as e:
        print (f"❌ Crossfade error: {e}", "🔥")

def register():
    return {
        "crossfade": crossfade
    }
