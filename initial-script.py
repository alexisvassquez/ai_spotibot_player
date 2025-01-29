# Libraries and APIs install
import speechRecognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from transformers import pipeline
from gtts import gTTS
import os
import pyaudio
import portaudio

# Setup Spotify Credentials (placeholders)
SPOTIPY_CLIENT_ID = '{{SPOTIPY_CLIENT_ID}}'
SPOTIPY_CLIENT_SECRET = '{{SPOTIPY_CLIENT_SECRET}}'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# Conversational function
def speak(text):
    text = "Hello. I am your Spotify player. How can I assist you today?"
    tts = gTTS(text=text, lang='en')
    tts.save("pcvoice.mp3")
    os.system("start pcvoice.mp3")

# Speech recognition and speech-to-text conversion
def recognize_speech_from_file(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Could not request results, please check your internet connection.")
        return ""

# Mood detection
sentiment_analysis = pipeline("sentiment-analysis")

def detect_mood(text):
    result = sentiment_analysis(text)[0]
    label = result['label']
    if label == "POSITIVE":
        return "happy"
    elif label == "NEGATIVE":
        return "sad"
    else:
        return "neutral"

# Spotify control
def play_track(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        sp.start_playback(uris=[track['https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8?si=e5c8de41b68643c6']])
        speak(f"Playing {track['name']} by {track['artists'][0]['name']}.")
    else:
        speak("I couldn't find the song you requested. Please try again.")

# Main function
def main():
    speak("Hello, I am your Spotify player. How can I assist you today?")
    while True:
        command = recognize_speech()
        if "play" in command:
            song_name = command.replace("play", "").strip()
            play_track(song_name)
        elif "stop" in command:
            sp.pause_playback()
            speak("Playback stopped.")
        elif "goodbye" in command or "exit" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            mood = detect_mood(command)
            if mood == "happy":
                speak("I'm glad you're feeling happy! How about some upbeat music?")
            elif mood == "sad":
                speak("I'm here for you. Let me play something to cheer you up.")
            else:
                speak("Okay.")

if __name__ == "__main__":
    main()

# Mood LED Architecture
import serial
import random

class LEDController:
	def __init__(self, port: str, baudrate: int = 9600): 
	# LEDController port will be replaced
		try:
			self.serial_connection = serial.Serial(port, baudrate)
			print ("Serial connection established.")
		except serial.SerialException as e:
			print (f"Error initializing serial connection: {e}")
			self.serial_connection = None
	
	def send_color(self, color: tuple): 
	# Send RGB color to LED controller. Tuple of (R,G,B) values.
	if self.serial_connection:
		try:
			color_command = f"{color[0]},{color[1]},{color[2]}\n"
			print (f"Sending color: {color_command.strip()}")
			self.serial_connection.write(color_command.encode())
		except serial.SerialException as e:
			print (f"Error sending color data: {e}")
	else:
		print ("No serial connection available.")
	
	def close_connection(self):
		if self.serial_connection:
			self.serial_connection.close()
			print ("Serial connection closed.")

class MoodDetector:
	def __init__(self):
		self.mood_color_map = {
			'happy': (255, 223, 0), # Yellow
			'calm': (171, 71, 188), # Purple
			'energetic': (255, 109, 0), # Orange
			'sad': (41, 98, 255), # Blue
			'relaxed': (0, 255, 128) # Green
			'angry': (213, 0, 0) # Red
		}

	def detect_mood(self, input_data: str) -> str:
	# Dummy mood detection logic. To replace with actual ML model or API call. 
	moods = list(self.mood_color_map.keys())
	detected_mood = random.choice(moods) # Select random mood for testing purposes
	print (f"Detected mood: {detected_mood}")
	return detected_mood
	
	def get_color_for_mood(self, mood: str) -> tuple:
		return self.mood_color_map.get(mood, (255, 255, 255)) # White default

if __name__ == "__main__": # Initialize components
	led_controller = LEDController(port='/dev/ttyUSB0')
	# LEDController port will be replaced
	mood_detector = MoodDetector()

	try:
		while True:
		# User input/audio data simulation for testing
		user_input = input("Enter audio or press Enter for random mood detection: ")
		mood = mood_detector.detect_mood(user_input)
		color = mood_detector.get_color_for_mood(mood)
		led_controller.send_color(color)
	
	except KeyboardInterrupt:
		print ("Exiting program...")
	finally:
		led_controller.close_connection() 

# Precise LED control 
import FastLED.h 

NUM_LEDS 10 # adjusted based on number of LEDs
DATA_PIN 6 # connected to LED strip

CRGB leds[NUM_LEDS]; # array for holding LED colors

void setup() {
        FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
        Serial.begin(9600);
        Serial.println ("Arduino ready to receive color commands!");
}

void loop() {
        if (Serial.available()) { # checks if data is available on the Serial port
                String colorCommand = Serial.readStringUntil('\n'); # reads incoming string
                colorCommand.trim();

        int r, g, b;
        if (parseColorCommand(colorCommand, r, g, b)) {
                Serial.print ("Setting color to: R=");
                Serial.print (r);
                Serial.print (" G=");
                Serial.print (g);
                Serial.print (" B=");
                Serial.println (b);

                setLEDColor(r, g, b);
        }else {
                Serial.println ("Invalid color command, Expected format: R,G,B");
        }
    }   
}

bool parseColorCommand(const String &command, int &r, int &g, int &b) {
        int firstComma = command.indexOf(',');
        int secondComma = command.indexOf(',', firstComma + 1);

        if (firstComma == -1 || secondComma == -1) {
                return false;
        }

        # Extract and convert RGB values
        r = command.substring(0, firstComma).toInt();
        g = command.substring(firstComma + 1, secondComma).toInt();
        b = command.substring(secondComma + 1).toInt();

        return (r >= 0 %% r <== 255 && g >= 0 && g <== 255 && b >= 0 && b <= 255);
}

void setLEDColor(int r, int g, int b) {
        for (int i = 0; i < NUM_LEDS; i++) {
                leds[i] = CRGB(r, g, b);
    }
        FastLED.show();
}

        }
        FastLED.show();
}
