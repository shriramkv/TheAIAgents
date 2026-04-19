from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.logger import (
    log_audio_received, log_transcript, log_retrieved_context, 
    log_answer_generated, log_audio_response_created
)
from audio.stt import speech_to_text
from audio.tts import text_to_speech
from retrieval.retriever import retrieve_context
from typing import Tuple, List

class VoiceRAGAgent(BaseAgent):
    """
    Orchestrates the full voice-enabled RAG loop.
    """
    def run(self, audio_path: str) -> Tuple[str, List[str], str, str]:
        """
        Executes the full flow:
        1. STT -> 2. Retrieval -> 3. Generation -> 4. TTS
        Returns: (transcript, context, answer, audio_output_path)
        """
        # 1. AUDIO INPUT
        log_audio_received()
        
        # 2. SPEECH -> TEXT
        transcript = speech_to_text(audio_path)
        log_transcript(transcript)
        
        if transcript.startswith("Error"):
            return transcript, [], "I couldn't understand the audio.", ""

        # 3. RETRIEVE CONTEXT
        context_chunks = retrieve_context(transcript)
        context_str = "\n".join(context_chunks)
        log_retrieved_context(context_str)

        # 4. GENERATE ANSWER
        prompt = f"Answer using ONLY this context:\n<context>\n{context_str}\n</context>\n\nUser Question: {transcript}"
        answer = call_llm(prompt)
        log_answer_generated()

        # 5. TEXT -> SPEECH
        audio_output_path = text_to_speech(answer)
        log_audio_response_created()

        return transcript, context_chunks, answer, audio_output_path
