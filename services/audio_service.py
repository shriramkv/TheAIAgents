import os
from datetime import datetime

def make_session_id():
    """Helper to generate unique IDs for audio files."""
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

class AudioService:
    """
    Service for handling Audio operations:
    - Speech-to-Text (STT) using OpenAI Whisper
    - Text-to-Speech (TTS) using OpenAI TTS
    """
    def __init__(self, client):
        """
        Initialize with an OpenAI client.
        
        Args:
            client: OpenAI client instance
        """
        self.client = client

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using Whisper.
        
        Args:
            audio_path (str): Path to the audio file.
            
        Returns:
            str: Transcribed text or empty string on failure.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""

    def generate_audio(self, text: str) -> str:
        """
        Generate audio from text using OpenAI TTS.
        
        Args:
            text (str): Text to convert to speech.
            
        Returns:
            str: Path to the generated MP3 file or empty string on failure.
        """
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            output_path = f"output_{make_session_id()}.mp3"
            response.stream_to_file(output_path)
            return output_path
        except Exception as e:
            print(f"Error generating audio: {e}")
            return ""
