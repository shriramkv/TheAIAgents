import gradio as gr
from agent import ToolCallingAgent

def run_agent(user_input: str):
    """
    Runs ToolCallingAgent and catches any errors.
    
    Args:
        user_input: Text from UI
        
    Returns:
        tuple containing (Final Answer block, Reasoning Logs block)
    """
    if not user_input.strip():
        return "Please enter a valid query.", "No query provided."
        
    agent = ToolCallingAgent()
    try:
        final_answer, full_log = agent.run(user_input)
        return final_answer, full_log
    except Exception as e:
        # Gracefully handle API errors or connection issues
        return f"Error running agent: {str(e)}", f"Exception detail:\n{str(e)}"

# Define the user layout cleanly applying Gradio standards
with gr.Blocks(title="🛠 Tool-Calling Agent", theme=gr.themes.Base()) as app:
    gr.Markdown(
        """
        # 🛠 Tool-Calling Agent
        This agent uses OpenAI's tool-calling capabilities to dynamically decide when to utilize different custom tools (calculator, string formatting, datetime).
        """
    )
    
    with gr.Row():
        input_box = gr.Textbox(
            label="Enter your query", 
            placeholder="e.g. What is 25 * 18 and reverse hello?",
            scale=4
        )
    
    submit_btn = gr.Button("Run Agent", variant="primary")
    
    gr.Markdown("### Results")
    with gr.Column():
        answer_output = gr.Textbox(label="Final Answer", interactive=False)
        logs_output = gr.Textbox(label="Reasoning Trace", lines=12, interactive=False)
        
    # Connect input box and button to execution function
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[answer_output, logs_output]
    )

if __name__ == "__main__":
    app.launch()
