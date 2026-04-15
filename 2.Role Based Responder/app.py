import gradio as gr
from dotenv import load_dotenv
from agent import RoleBasedAgent
from shared.utils import load_yaml
import os

# Load Environment variables (OPENAI_API_KEY)
load_dotenv()

# Load Global Config
try:
    global_config = load_yaml("config.yaml")
except Exception as e:
    print(f"Warning: Could not load config.yaml ({e}). Proceeding with empty config.")
    global_config = {}

def run_agent(user_input: str, role: str) -> tuple[str, str]:
    """
    Initializes the RoleBasedAgent with the selected role and runs the query.
    
    Args:
        user_input (str): The user's question or prompt.
        role (str): The selected role from the dropdown.
        
    Returns:
        tuple[str, str]: The LLM's final response and the reasoning logs.
    """
    if not user_input.strip():
        return "Please enter a query.", "No query provided."
        
    if not os.getenv("OPENAI_API_KEY"):
        return "System configuration error.", "OPENAI_API_KEY is missing. Please check your .env file."
        
    try:
        agent = RoleBasedAgent(config=global_config, role_name=role)
        # Agent's run loop handles the Think -> Act -> Observe logic 
        response, logs = agent.run(user_input)
        return response, logs
    except Exception as e:
        return f"An error occurred: {str(e)}", "Error during execution."

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(), title="Role-Based Responder") as app:
    gr.Markdown("# 🎭 Role-Based Responder")
    gr.Markdown("Select a persona to see how the system prompt influences the AI's reasoning and final output.")
    
    with gr.Row():
        with gr.Column(scale=1):
            role_selector = gr.Dropdown(
                choices=["Teacher", "Lawyer", "Startup Founder", "Default"],
                value="Teacher",
                label="Select Role"
            )
            input_box = gr.Textbox(
                label="Enter your query", 
                placeholder="e.g., Explain the concept of blockchain...",
                lines=3
            )
            submit_btn = gr.Button("Generate Response", variant="primary")
            
        with gr.Column(scale=2):
            answer_output = gr.Textbox(label="Final Response", lines=6)
            logs_output = gr.Textbox(label="Reasoning Logs", lines=10)

    # Link button click to the agent runner
    submit_btn.click(
        fn=run_agent,
        inputs=[input_box, role_selector],
        outputs=[answer_output, logs_output]
    )

if __name__ == "__main__":
    print("Starting Role-Based Responder application...")
    app.launch()
