# Necessary APIs (pip install)
import speech_recognition as sr
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
    results = sp.search(q=song_name, limit=1, type='track') # type: ignore
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        sp.start_playback(uris=[track['https://open.spotify.com/track/4SJrFfeVaEWXdB5qUa6h1G?si=9fbaf1a4c4124953']])
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
