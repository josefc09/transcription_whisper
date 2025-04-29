import whisper
import os
import sys
import tempfile
import subprocess
from pydub import AudioSegment

def download_audio_from_url(url):
    """Downloads audio from a video URL"""
    temp_dir = tempfile.mkdtemp()
    output_path_template = os.path.join(temp_dir, "audio.%(ext)s")

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_path_template,
        url
    ]

    print("Downloading audio from URL...")
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Error downloading the audio. yt-dlp failed.")
        print("Details:", e.stderr.decode())
        sys.exit(1)

    # Attempt to locate the downloaded mp3 file
    downloaded_file = os.path.join(temp_dir, "audio.mp3")
    if not os.path.exists(downloaded_file):
        print("Download failed: audio file was not created.")
        sys.exit(1)

    print(f"Audio downloaded to: {downloaded_file}")
    return downloaded_file

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
        
def main(input_source, output_path):

    if input_source.startswith("http://") or input_source.startswith("https://"):
        audio_path = download_audio_from_url(input_source)
    else:
        if not os.path.exists(input_source):
            print(f"Error: The file '{input_source}' does not exist.")
            sys.exit(1)
        audio_path = input_source

    if not audio_path.endswith(".wav"):
        audio_path = convert_audio_to_wav(audio_path)

    text = transcribe_audio(audio_path)
    save_transcription(text, output_path)
    print(f"Transcription saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transcriber.py <input_audio_path_or_url> <output_text_path>")
        sys.exit(1)

    input_audio_or_url = sys.argv[1]
    output_file = sys.argv[2]

    main(input_audio_or_url, output_file)