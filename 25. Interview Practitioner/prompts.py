# prompts.py
from typing import List

SYSTEM_BASE = (
    "You are an expert interview coach and interviewer. You must behave like a professional interviewer: "
    "ask clear, concise interview questions, probe with follow-ups, and provide actionable feedback at the end. "
)

ROLE_BRIEFS = {
    "software_engineer": "Role: Software Engineer. Expect questions about data structures, algorithms, system design, and behavioral questions.",
    "data_scientist": "Role: Data Scientist. Expect statistics, ML model design, feature engineering, and product-sense questions.",
    "sales": "Role: Sales. Expect situational questions, roleplay, objection handling, and metrics-focused behavioral questions.",
}


def build_system_prompt(role: str) -> str:
    """
    Construct the system prompt based on the interview role.
    """
    role_brief = ROLE_BRIEFS.get(role, "Role: general")
    return SYSTEM_BASE + " " + role_brief

def build_next_question_prompt(history: List[dict], role: str, difficulty: str, resume_text: str = "") -> List[dict]:
    """
    Construct the prompt for generating the next interview question.
    
    Args:
        history: List of previous Q&A pairs.
        role: The target role.
        difficulty: The difficulty level.
        resume_text: Optional resume content.
        
    Returns:
        List[dict]: Messages for the LLM.
    """
    system = build_system_prompt(role)
    system += f"\nDifficulty Level: {difficulty}"
    
    if resume_text:
        system += f"\n\nCandidate Resume:\n{resume_text}\n"
        system += "Note: You have access to the candidate's resume. Tailor your questions to their specific experience and projects when appropriate."
    
    system += (
        "\nYour task is to generate the NEXT interview question based on the conversation history.\n"
        "Rules:\n"
        "1. If the previous answer was vague or insufficient, ask a follow-up question.\n"
        "2. If the previous topic is exhausted, switch to a new relevant topic (e.g., from Behavioral to Technical).\n"
        "3. Keep questions concise and professional.\n"
        "4. Do NOT repeat questions.\n"
        "5. If the interview has gone on for long enough (e.g. 5-6 questions), you can start wrapping up.\n"
        "Output ONLY the question text."
    )
    
    messages = [{"role": "system", "content": system}]
    
    # Add history context
    for item in history:
        messages.append({"role": "assistant", "content": item["question"]})
        if "answer" in item:
            messages.append({"role": "user", "content": item["answer"]})
            
    messages.append({"role": "system", "content": "Generate the next question now."})
    return messages

def build_feedback_prompt(answer: str, question_text: str, role: str) -> List[dict]:
    """
    Construct the prompt for evaluating an answer.
    """
    system = build_system_prompt(role)
    user = (
        "You are the interviewer. The candidate answered the following to the question:\n"
        f"Question: {question_text}\nAnswer: {answer}\n\n"
        "Provide: (1) A short bullet list: strengths, (2) Areas to improve with concrete suggestions, (3) A numeric score (0-10) and confidence (low/med/high)."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

