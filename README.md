# Audio Transcriber using Whisper and Pydub

This Python script converts an audio file (e.g., MP3, WAV) into text using [OpenAI Whisper](https://github.com/openai/whisper) for transcription and [Pydub](https://github.com/jiaaro/pydub) for audio format conversion. You provide the input audio file and the desired path for the output text file via command-line arguments.

## Features

- Automatically converts various audio formats (MP3, M4A, etc.) to WAV
- Transcribes audio using the Whisper `small` model
- Saves the output transcription to a file you specify

## How to use

```bash
pip install -r requirements.txt
python3 audioToText.py "file.mp3" "transcription.txt"
```