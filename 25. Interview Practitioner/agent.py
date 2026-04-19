# agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Initialize client - it will automatically check OPENAI_API_KEY environment variable
client = OpenAI()
from typing import Dict, Any, List
from prompts import build_next_question_prompt, build_feedback_prompt
from utils import InterviewSession, make_session_id, save_session
from services.audio_service import AudioService
from services.report_service import ReportService

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

class InterviewAgent:
    """
    Core agent that manages the interview process, state, and interaction with LLM services.
    """
    def __init__(self, role: str, difficulty: str = "medium", resume_text: str = ""):
        """
        Initialize the InterviewAgent.
        
        Args:
            role (str): The role to interview for (e.g., "software_engineer").
            difficulty (str): Difficulty level ("easy", "medium", "hard").
            resume_text (str): Optional text content of the candidate's resume.
        """
        self.role = role
        self.difficulty = difficulty
        self.resume_text = resume_text
        self.history = [] # List of {"question": str, "answer": str}
        
        # Initialize Services
        self.audio_service = AudioService(client)
        self.report_service = ReportService(client, MODEL)

    def generate_question(self) -> Dict[str, Any]:
        """
        Generate the next interview question based on history and resume.
        
        Returns:
            Dict[str, Any]: Contains 'question' object and 'agent_text'.
        """
        # If history is empty, start with a standard opening
        if not self.history:
            if self.resume_text:
                q_text = "I see you have uploaded your resume. Can you walk me through your background, highlighting your most relevant experience?"
            else:
                q_text = "Tell me about yourself and your background."
        else:
            messages = build_next_question_prompt(self.history, self.role, self.difficulty, self.resume_text)
            resp = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=200)
            content = resp.choices[0].message.content
            q_text = content.strip() if content else "Do you have any questions for me?"

        return {"question": {"text": q_text}, "agent_text": q_text}

    def evaluate_answer(self, question_text: str, answer_text: str) -> Dict[str, Any]:
        """
        Evaluate the user's answer and provide feedback.
        
        Args:
            question_text (str): The question asked.
            answer_text (str): The user's answer.
            
        Returns:
            Dict[str, Any]: Contains 'feedback' string.
        """
        messages = build_feedback_prompt(answer_text, question_text, self.role)
        resp = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=500)
        content = resp.choices[0].message.content
        text = content.strip() if content else ""
        return {"feedback": text, "raw": resp}

    def transcribe_audio(self, audio_path: str) -> str:
        """Delegate to AudioService."""
        return self.audio_service.transcribe_audio(audio_path)

    def generate_audio(self, text: str) -> str:
        """Delegate to AudioService."""
        return self.audio_service.generate_audio(text)

    def generate_final_report(self) -> str:
        """Delegate to ReportService."""
        return self.report_service.generate_final_report(self.history)

    def run_interview(self, user_responses: List[str]) -> Dict[str, Any]:
        # Deprecated batch mode
        pass

