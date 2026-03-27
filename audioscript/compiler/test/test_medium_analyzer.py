# ai_spotibot_player
# AudioMIX
# audio/ai/compiler/test/test_medium_analyzer.py

# Test stub for mid-complex analyzer

from audio.ai.compiler.audio2script.analyzer import analyze_audio

def main():
    frames, sections, bpm = analyze_audio("audio/samples/full/cvltiv8r_clean.wav")    # sample audio file
    print ("BPM:", bpm)
    print ("Sections:", sections[:3])
    print ("Frames:", len(frames))

if __name__ == "__main__":
    main()
