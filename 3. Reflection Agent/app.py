import gradio as gr
from agent import ReflectionAgent

# Initialize the agent instance
agent = ReflectionAgent()

def run_agent(user_input: str):
    """
    Runs the ReflectionAgent end-to-end for a given user input.
    Returns the initial response, critique, improved response, and flow logs.
    """
    # Prevent empty inputs from calling the LLM
    if not user_input.strip():
        return "Please enter a valid query.", "", "", "Error: Empty input."
        
    initial, critique, improved, logs = agent.run(user_input)
    return initial, critique, improved, logs

# Define the Gradio UI using Blocks
with gr.Blocks(title="Reflection Agent") as app:
    gr.Markdown("# 🔁 Reflection Agent")
    gr.Markdown("An AI Assistant that generates an answer, critiques itself, and produces an improved result.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_box = gr.Textbox(label="Enter your query", placeholder="E.g., Write a blog about AI...", lines=3)
            submit_btn = gr.Button("Run Reflection", variant="primary")
            
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("Results"):
                    initial_output = gr.Textbox(label="🧾 Initial Response", lines=5, interactive=False)
                    critique_output = gr.Textbox(label="🔍 Critique", lines=5, interactive=False)
                    improved_output = gr.Textbox(label="✨ Improved Response", lines=8, interactive=False)
                
                with gr.TabItem("Execution Logs"):
                    logs_output = gr.Textbox(label="📜 Logs", lines=15, interactive=False)
    
    # Event wiring
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[
            initial_output,
            critique_output,
            improved_output,
            logs_output
        ]
    )

if __name__ == "__main__":
    # Launch the Gradio web server
    app.launch()
