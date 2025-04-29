import whisper
import os
import sys
from pydub import AudioSegment

def convert_audio_to_wav(audio_path):
    """Converts an audio file to WAV format."""
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio(audio_path):
    """Transcribes an audio file to text using Whisper."""
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["text"]

def save_transcription(text, output_path):
    """Saves the transcribed text to a file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def main(audio_path, output_path):
    """Main function: handles conversion, transcription, and saving output."""
    if not audio_path.endswith(".wav"):
        audio_path = convert_audio_to_wav(audio_path)

    text = transcribe_audio(audio_path)
    save_transcription(text, output_path)
    print(f"Transcription saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcriber.py <input_audio_path> <output_text_path>")
        sys.exit(1)

    input_audio = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_audio):
        print(f"Error: The file '{input_audio}' does not exist.")
        sys.exit(1)

    main(input_audio, output_file)
