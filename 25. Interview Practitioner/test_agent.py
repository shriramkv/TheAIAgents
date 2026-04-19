from agent import InterviewAgent

def test_dynamic_flow():
    print("Initializing Agent...")
    agent = InterviewAgent(role="software_engineer", difficulty="medium")
    
    # 1. Generate First Question
    print("\n--- Step 1: First Question ---")
    q1 = agent.generate_question()
    print(f"Agent: {q1['agent_text']}")
    assert q1['agent_text'], "Agent should generate a question"
    
    # 2. Simulate Answer
    user_ans = "I am a software engineer with 5 years of experience in Python."
    print(f"\nUser: {user_ans}")
    
    # Update history
    agent.history.append({"question": q1['question']['text'], "answer": user_ans})
    
    # 3. Generate Next Question (Should be a follow-up or relevant technical question)
    print("\n--- Step 2: Second Question ---")
    q2 = agent.generate_question()
    print(f"Agent: {q2['agent_text']}")
    assert q2['agent_text'], "Agent should generate a second question"
    assert q2['agent_text'] != q1['agent_text'], "Questions should not repeat immediately"
    
    # 4. Evaluate Answer
    print("\n--- Step 3: Evaluation ---")
    eval_ = agent.evaluate_answer(q1['question']['text'], user_ans)
    print(f"Feedback: {eval_['feedback']}")
    assert eval_['feedback'], "Feedback should be generated"

if __name__ == "__main__":
    test_dynamic_flow()
