import os
from openai import OpenAI
from shared.utils import load_config, get_env_var

def speech_to_text(audio_file_path: str) -> str:
    """
    Convert speech to text using OpenAI Whisper API.
    """
    if not audio_file_path or not os.path.exists(audio_file_path):
        return "Error: Audio file not found."

    config = load_config()
    stt_model = config.get("stt_model", "whisper-1")
    client = OpenAI(api_key=get_env_var("OPENAI_API_KEY"))

    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"
