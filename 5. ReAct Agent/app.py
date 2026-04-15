import gradio as gr
from agent import ReActAgent

def run_agent(user_input: str) -> tuple[str, str]:
    """
    Runs the ReAct Agent and returns (final_answer, full_trace)
    """
    if not user_input.strip():
        return "Please enter a valid query.", "No query provided."
        
    agent = ReActAgent()
    final_answer, full_trace = agent.run(user_input)
    return final_answer, full_trace

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🔍 ReAct Loop Tracer")
    gr.Markdown(
        "This tool executes an Agentic AI using the **ReAct (Reasoning and Acting)** pattern. "
        "It visibly exposes its entire inner monologue, highlighting exactly how it thinks and what tools it uses."
    )
    
    with gr.Row():
        input_box = gr.Textbox(
            label="Enter your query", 
            placeholder="e.g., Use the calculator to find what is 5 * 13, and then search for the capital of France.",
            lines=2
        )
        
    submit_btn = gr.Button("Run ReAct Agent", variant="primary")
    
    with gr.Row():
        answer_output = gr.Textbox(label="Final Answer", lines=4)
        
    with gr.Row():
        trace_output = gr.Textbox(label="Reasoning Trace", lines=15)
        
    # Connect Interactions
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[answer_output, trace_output]
    )

if __name__ == "__main__":
    # Ensure dependencies and keys are somewhat warned if missing but proceed
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY missing from environment. API calls will fail.")
        
    app.launch(server_name="0.0.0.0", server_port=7860)
