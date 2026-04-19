import gradio as gr
from agent import InterviewAgent
from utils import make_session_id, extract_text_from_pdf

# Constants for UI
ROLES = ["software_engineer", "data_scientist", "sales"]
DIFFICULTIES = ["easy", "medium", "hard"]

def start_interview(role, difficulty, resume_file):
    """
    Initialize the interview session.
    """
    resume_text = ""
    if resume_file:
        resume_text = extract_text_from_pdf(resume_file.name)
        
    agent = InterviewAgent(role=role, difficulty=difficulty, resume_text=resume_text)
    # Generate first question
    first = agent.generate_question()
    
    # State now stores the agent instance and the current question
    state = {
        "agent": agent,
        "current_question": first["question"],
        "session_id": make_session_id(),
        "buffer": []
    }
    
    chat_history = [{"role": "assistant", "content": first["agent_text"]}]
    return chat_history, state

def submit_answer(state, user_answer, audio_input, chat_history):
    """
    Process user answer (text or audio) and generate response.
    """
    if not state:
        return "Please start the interview first.", chat_history, None, "", None

    agent: InterviewAgent = state["agent"]
    
    # Handle Audio Input
    if audio_input:
        transcribed = agent.transcribe_audio(audio_input)
        if transcribed:
            user_answer = transcribed
    
    if not user_answer:
        return "Please provide an answer (text or audio).", chat_history, state, "", None

    current_q = state["current_question"]
    
    # Evaluate answer
    eval_ = agent.evaluate_answer(current_q["text"], user_answer)
    
    # Update agent history
    agent.history.append({
        "question": current_q["text"],
        "answer": user_answer,
        "feedback": eval_["feedback"]
    })
    
    # Update buffer for session saving (optional, could be done in agent)
    state["buffer"].append({
        "question": current_q["text"],
        "answer": user_answer,
        "feedback": eval_["feedback"]
    })
    
    # Update chat history
    if chat_history is None:
        chat_history = []
    chat_history.append({"role": "user", "content": user_answer})
    
    # Generate next question
    next_q_data = agent.generate_question()
    next_q_text = next_q_data["agent_text"]
    
    # Generate Audio Response
    audio_output = agent.generate_audio(next_q_text)
    
    # Update state with new question
    state["current_question"] = next_q_data["question"]
    
    chat_history.append({"role": "assistant", "content": next_q_text})
    
    return eval_["feedback"], chat_history, state, "", audio_output

def end_interview(state):
    """
    Generate and return the final report.
    """
    if not state:
        return "No active interview."
        
    agent: InterviewAgent = state["agent"]
    report = agent.generate_final_report()
    return report
