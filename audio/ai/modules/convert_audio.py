from pydub import AudioSegment
import tempfile

def convert_to_wav(input_path):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(44100).set_channels(2).normalize()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        audio.export(temp_wav.name, format="wav")
        return temp_wav.name
