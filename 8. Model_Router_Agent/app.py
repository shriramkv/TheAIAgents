import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from agent import ModelRouterAgent

# Initialize the agent
agent = ModelRouterAgent()

def run_agent(user_input: str):
    """
    Gradio execution wrapper. 
    Returns: response, routing_info, logs
    """
    if not user_input.strip():
        return "Please provide an input.", "", "Error: Empty input provided."
    return agent.run(user_input)

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🔀 Model Router Agent")
    gr.Markdown("An intelligent agent that dynamically routes queries based on complexity to optimize cost and performance, with built-in reliability and fallback mechanisms.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_box = gr.Textbox(
                label="Enter your query", 
                placeholder="e.g. What is 2+2? or Explain quantum computing in detail...",
                lines=4
            )
            submit_btn = gr.Button("Run Router", variant="primary")
            
        with gr.Column(scale=2):
            response_output = gr.Textbox(label="Response", lines=8, interactive=False)
            routing_output = gr.Textbox(label="Routing Decision", lines=2, interactive=False)

    with gr.Row():
        logs_output = gr.Textbox(label="Logs", lines=12, interactive=False)

    # Wire up interactions
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[response_output, routing_output, logs_output]
    )

if __name__ == "__main__":
    # Launch interface
    app.launch(server_name="0.0.0.0", server_port=7860)
