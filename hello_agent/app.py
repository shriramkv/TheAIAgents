"""
Gradio UI entrypoint for the Hello Agent.
"""
import gradio as gr
from dotenv import load_dotenv

# Load environment variables before importing anything that needs them
load_dotenv()

from agent import HelloAgent

# Initialize the agent
agent = HelloAgent()

def run_agent(user_input: str):
    """
    Calls HelloAgent and returns:
    - final answer
    - logs as string
    """
    if not user_input.strip():
        return "Please enter a query.", "No logs."

    answer, logs = agent.run(user_input)
    return answer, logs

# Gradio layout setup
with gr.Blocks(theme=gr.themes.Soft(), title="🤖 Hello Agent") as app:
    gr.Markdown("# 🤖 Hello Agent")
    gr.Markdown("A clean, modular, production-quality basic AI Agent.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_box = gr.Textbox(label="Enter your query", placeholder="e.g., 25 * 18, reverse hello, or What is AI?")
            submit_btn = gr.Button("Run Agent", variant="primary")
            
            gr.Examples(
                examples=["25 * 18", "reverse hello", "What is AI?"],
                inputs=input_box
            )
            
        with gr.Column(scale=1):
            answer_output = gr.Textbox(label="Final Answer", interactive=False)
            logs_output = gr.Textbox(label="Reasoning Trace", lines=10, interactive=False)

    # Wire up the button
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[answer_output, logs_output]
    )

if __name__ == "__main__":
    app.launch()
