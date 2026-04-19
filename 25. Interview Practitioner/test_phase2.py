from agent import InterviewAgent
from utils import extract_text_from_pdf
import os

def test_phase2():
    print("--- Testing Phase 2 Features ---")
    
    # 1. Test Resume Logic (Mock)
    print("\n1. Testing Resume Logic...")
    agent = InterviewAgent(role="software_engineer", resume_text="Experienced in Python and AI.")
    q1 = agent.generate_question()
    print(f"Initial Question (with resume): {q1['agent_text']}")
    assert "resume" in q1['agent_text'].lower() or "background" in q1['agent_text'].lower(), "Should reference resume/background"

    # 2. Test Audio Generation
    print("\n2. Testing Audio Generation...")
    audio_path = agent.generate_audio("Hello, this is a test.")
    print(f"Generated Audio Path: {audio_path}")
    assert audio_path and audio_path.endswith(".mp3"), "Should generate MP3 file"
    # Clean up
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # 3. Test Report Generation
    print("\n3. Testing Report Generation...")
    # Mock history
    agent.history = [
        {"question": "Tell me about yourself.", "answer": "I am a coder.", "feedback": "Good."},
        {"question": "What is Python?", "answer": "A language.", "feedback": "Brief."}
    ]
    report = agent.generate_final_report()
    print("Report Generated (First 100 chars):", report[:100])
    assert "Executive Summary" in report or "Strengths" in report, "Report should contain key sections"

if __name__ == "__main__":
    test_phase2()
