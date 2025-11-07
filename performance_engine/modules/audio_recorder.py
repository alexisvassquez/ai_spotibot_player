# ai_spotibot_player
# AudioMIX
# performance_engine/modules/audio_recorder.py

import threading
import time
from typing import Optional
import wave
import pyaudio

try:
    from performance_engine.modules.shared import say
except ImportError:
    # fallback for direct testing
    def say(msg, icon=""):
        print (f"{icon} {msg}")

# Singleton-style recorder
class PyAudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.running = False

        self.device_index = None    # sys default
        self.format = pyaudio.paInt16
        self.samplerate = 48000     # safe default on Linux
        self.channels = 1           # default start at mono; can be set to 2
        self.chunk = 1024

    def start(self, filename):
        if self.running:
            say(" [record] already running; stop first", "⚠️")
            return

        try:
            #open input stream
            self.stream = self.audio.open(
                format=self.format,
                rate=self.samplerate,
                channels=self.channels,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.chunk
            )
            self.frames = []
            self.running = True
            say(f" [record] started -> {filename} @ {self.samplerate} Hz / ch={self.channels}", "⏺️")

            def _record_loop():
                while self.running:
                   try:
                       data = self.stream.read(self.chunk, exception_on_overflow=False)
                       self.frames.append(data)
                   except Exception as e:
                       say(f" [record] error: {e}", "❌")
                       break

            self.thread = threading.Thread(target=_record_loop, daemon=True)
            self.thread.start()
            self.filename = filename

        except Exception as e:
            say(f" [record] failed to start: {e}", "❌")

    def stop(self):
        if not self.running:
            say(" [record] not running", "⚠️")
            return

        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.samplerate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        say(f" [record] stopped and saved -> {self.filename}", "⏹️")

    def oneshot(self, filename, seconds):
        try:
            seconds = float(seconds)
            if seconds <= 0:
                raise ValueError("Seconds must be > 0")
        except Exception as e:
            say(f"  [record] invalid duration: {e}", "❌")
            return

        self.start(filename)

        def _stop_later():
            try:
                for remaining in range(int(seconds), 0, -1):
                    print (f"  [⏳] {remaining} sec remaining...", end="\r")
                    time.sleep(1)
                self.stop()
            except Exception as e:
                say(f"  [record] oneshot error: {e}", "❌")

        t = threading.Thread(target=_stop_later, daemon=True)
        t.start()
        return t    # handy for programmatic calls

    def set_input(self, index):
        self.device_index = int(index) if index else None
        say(f" [record] input device set to: {self.device_index}", "🎤")

    def set_format(self, rate=None, channels=None):
        if rate: self.rate = int(rate)
        if channels: self.channels = int(channels)
        say(f" [record] format -> {self.rate} Hz / ch={self.channels}", "🎚️")

    def list_inputs(self):
        count = self.audio.get_device_count()
        say("Input devices:", "🎤")
        for i in range(count):
            info = self.audio.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                say(f" [{i}] {info['name']} (ch={info['maxInputChannels']})")

REC = PyAudioRecorder()

# AudioScript (AS) Commands
def record(*args):
    if not args:
        say(" [record] usage: record(\"out.wav\", seconds=optional)", "⚠️")
        return
    filename = args[0].strip().strip('"')
    seconds = float(args[1]) if len(args) > 1 else None
    if seconds:
        REC.oneshot(filename, seconds)
    else:
        REC.start(filename)

def record_stop(*_):
    REC.stop()

def record_set_input(*args):
    REC.set_input(args[0]) if args else None

def record_set_format(*args):
    rate = args[0] if len(args) > 0 else None
    channels = args[1] if len(args) > 1 else None
    REC.set_format(rate, channels)

def list_inputs(*_):
    REC.list_inputs()

def register():
    return {
        "record": record,
        "record_stop": record_stop,
        "record_set_input": record_set_input,
        "record_set_format": record_set_format,
        "list_inputs": list_inputs
    }

if __name__ == "__main__":
    REC.list_inputs()
    REC.set_input(0)    # or None
    REC.set_format(48000, 1)
    REC.oneshot("test_direct.wav", 5)
