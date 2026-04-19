# utils.py
import json
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime

SESSION_STORAGE = "sessions.json"

@dataclass
class InterviewSession:
    session_id: str
    role: str
    difficulty: str
    started_at: str
    history: List[dict]

    def to_dict(self):
        return asdict(self)

def load_sessions():
    """Load sessions from JSON storage."""
    try:
        with open(SESSION_STORAGE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_session(session: InterviewSession):
    """Save a session to JSON storage."""
    data = load_sessions()
    data[session.session_id] = session.to_dict()
    with open(SESSION_STORAGE, "w") as f:
        json.dump(data, f, indent=2)

def make_session_id():
    """Generate a unique session ID based on timestamp."""
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text.
    """
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
