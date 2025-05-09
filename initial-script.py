# Libraries and APIs install
import speechRecognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from transformers import pipeline
from gtts import gTTS
import os
import pyaudio
import portaudio.h
import serial
import random
import time
import arduino
import FastLED.h 
import librosa
import scikit-learn
import numpy as np
import joblib

# Setup Spotify Credentials (placeholders)
SPOTIPY_CLIENT_ID = '{{SPOTIFY_CLIENT_ID}}'
SPOTIPY_CLIENT_SECRET = '{{SPOTIFY_CLIENT_SECRET}}'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
# add wider range of scopes
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
    tts.save("male_robotic.mp3")
    os.system("start male_robotic.mp3")

# Speech recognition and speech-to-text conversion
def recognize_speech_from_file(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said: {command}")
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
        speak("Playing {track['name']} by {track['artists'][0]['name']}.")
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

# Start of Arduino control functionality
# Mood LED Architecture
class LEDController:
	def __init__(self, port: str, baudrate: int = 9600):  # LEDController port will be replaced
		try:
			self.serial_connection = serial.Serial(port, baudrate)
			print ("Serial connection established.")
		except serial.SerialException as e:
			print ("Error initializing serial connection: {e}")
			self.serial_connection = None

	# Send RGB color to LED controller. Tuple of (R,G,B) values.
	def send_color(self, color: tuple): 
	""
	Send RGB color to the LED controller.
	:param color: Tuple of (R, G, B) values.
	""
	if self.serial_connection:
		try:
			color_command = "{color[0]},{color[1]},{color[2]}\n"
			print ("Sending color: {color_command.strip()}")
			self.serial_connection.write(color_command.encode())
		except serial.SerialException as e:
			print ("Error sending color data: {e}")
	else:
		print ("No serial connection available.")
	
	# Sends lighting patterns to LED controller.
	def send_pattern(self, pattern_name: str):
	""
	Send predefined lighting pattern to the LED controller.
	:param pattern_name: Name of the lighting pattern.
	""
	if self.serial_connection:
		print (f"Sending pattern command: {pattern_name}") 
		self.serial_connection.write(f"PATTERN:{pattern_name}\n".encode())
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
			'relaxed': (0, 255, 128), # Green
			'angry': (213, 0, 0) # Red
		}
		self.mood_pattern_map = {
			'happy': 'blink',
			'calm': 'wave',
			'energetic': 'chase',
			'sad': 'fade',
			'relaxed': 'sparkle',
			'angry': 'strobe'
		}

	def detect_mood(self, input_data: str) -> str:
	# Dummy mood detection logic. To replace with actual ML model or API call. 
	moods = list(self.mood_color_map.keys())
	detected_mood = random.choice(moods) # Select random mood for testing purposes
	print ("Detected mood: {detected_mood}")
	return detected_mood
	
	def get_color_for_mood(self, mood: str) -> tuple:
		return self.mood_color_map.get(mood, (255, 255, 255)) # White default
	
	def get_pattern_for_mood(self, mood: str): 
		return self.mood_pattern_map.get(mood, 'solid') # Solid default
	
	def send_feedback(self, message: str):
		print ("Device feedback: {Success!}")

if __name__ == "__main__": # Initialize components
	led_controller = LEDController(port='/dev/ttyUSB0') # LEDController port will be replaced
	mood_detector = MoodDetector()

	try:
		while True:
		# User input/audio data simulation for testing
		user_input = input("Enter audio or press Enter for random mood detection: ")
		mood = mood_detector.detect_mood(user_input)
		color = mood_detector.get_color_for_mood(mood)
		pattern = mood_detector.get_pattern_for_mood(mood)
		led_controller.send_color(color)
		time.sleep(0.5) # brief delay before sending pattern
		led_controller.send_pattern(pattern)
	
	except KeyboardInterrupt:
		print ("Exiting program...")
	finally:
		led_controller.close_connection() 

# Precise LED hardware control 
def NUM_LEDS 10 # adjusted based on number of LEDs
def DATA_PIN 6 # connected to LED strip

CRGB leds[NUM_LEDS]; # array for holding LED colors

void setup() {
	FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS); # hardware control
	Serial.begin(9600); # LEDController serial port will be replaced
	Serial.println ("Arduino ready to receive color commands!");
}

void loop() {
	if (Serial.available()) { # checks if data is available on the serial port
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
	}
	else {
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
# End of Arduino control functionality

# ML model extraction and training
def extract_features(audio_path):
	y, sr = librosa.load(audio_path, duration=10) # loads first 10 secs of audio file
	
	# extract 13 mfccs and spectral contrast from librosa audio file. 
	mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
	mfccs_mean = np.mean(mfccs.T, axis=0)

	spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
	spectral_contrast_mean = np.mean(spectral_contrast.T, axis=0)

	# add the means of both functions into single array to equal its features 
	features = np.hstack([mfccs_mean, spectral_contrast_mean]) # total of 2 means
	return features

# Defining mood categories
MOODS = ['happy', 'calm', 'energetic', 'sad', 'relaxed', 'angry']

def extract_features(file_path):
	"""Extract MFCC, spectral contrast, and chroma features from an audio file."""
	y_audio, sr = librosa.load(file_path, sr=22050) # Load audio
	mfcc = librosa.feature.mfcc(y=y_audio, sr=sr, n_mfcc=13) # Extract mfcc
	spectral_contrast = librosa.feature.spectral_contrast(y=y_audio, sr=sr)
	chroma = librosa.feature.chroma_stft(y=y_audio, sr=sr) # chroma feat

	feature_vector = np.hstack([
		np.mean(mfcc, axis=1),
		np.mean(spectral_contrast, axis=1),
		np.mean(chroma, axis=1)
	])

	return feature_vector 

def load_dataset(data_dir):
	"""Loads dataset, extracts features, and assigns labels."""
	x = [] # features
	y = [] # labels
	
	for mood_idx, mood in enumerate(MOODS):
		mood_path = os.path.join(data_dir, mood)

		if not os.path.isdir(mood_path):
			continue
		
		for file in os.listdir(mood_path):
			if file.endswith(".wav"):
				file_path = os.path.join(mood_path,file)

			try:
				features = extract_feature(file_path)
				X.append(features)
				y.append(mood_idx) # stores mood index as label
			except Exception as e:
				print ("Error processing {file}: {e}")

		return np.array(X), np.array(y) 
		print ("Dataset Loaded: {X.shape[0]} samples with {X.shape[1]} features each")
	
	for mood_dir in os.listdir(data_dir):
		mood_path = os.path.join(data_dir, mood_dir)

	if os.path.isdir(mood_path):
		for file_name in os.listdir(mood_path):
			file_path = os.path.join(mood_path, file_name)

			try:
			    features.append(extract_features(file_path))
			    labels.append(happy) # uses folder name as label
			except Exception as e:
			    print (f"Error processing {file_path}: {e}")
		
		return np.array(features), np.array(labels)
