import os
from gtts import gTTS
import uuid

def text_to_speech(text: str) -> str:
    """
    Convert text to speech and save as audio file.
    Returns path to audio file.
    """
    if not text:
        return ""

    try:
        # Generate a unique filename to avoid conflicts
        filename = f"response_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join("audio", filename)
        
        # Ensure directory exists
        os.makedirs("audio", exist_ok=True)

        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        return ""
