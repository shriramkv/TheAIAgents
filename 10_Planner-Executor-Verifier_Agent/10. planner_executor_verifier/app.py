import gradio as gr
from agent import PlannerExecutorVerifierAgent

# Initialize the Planner-Executor-Verifier Agent
agent = PlannerExecutorVerifierAgent()

def run_agent(user_input: str):
    """
    Interface wrapper to trigger the agent pipeline.
    """
    if not user_input.strip():
        return "Please enter a task", "", "", "", "No input provided."
        
    return agent.process(user_input)

# Gradio Blocks define UI Layout and interaction
with gr.Blocks(title="Planner-Executor-Verifier Agent") as app:
    gr.Markdown("# 🧠 Planner–Executor–Verifier Agent")
    
    with gr.Row():
        input_box = gr.Textbox(label="Enter your task", placeholder="E.g., Write a business plan for a local bakery.", lines=2, scale=4)
        submit_btn = gr.Button("Run Agent", scale=1)
        
    with gr.Row():
        with gr.Column():
            plan_output = gr.Textbox(label="Plan", lines=6)
            exec_output = gr.Textbox(label="Execution Results", lines=10)
        
        with gr.Column():
            verify_output = gr.Textbox(label="Verification", lines=3)
            final_output = gr.Textbox(label="Final Answer", lines=13)
            
    logs_output = gr.Textbox(label="Logs", lines=12)

    # Event Connections
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[
            plan_output,
            exec_output,
            verify_output,
            final_output,
            logs_output
        ]
    )

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860)
