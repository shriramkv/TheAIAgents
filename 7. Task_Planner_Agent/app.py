import gradio as gr
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

from agent import TaskPlannerAgent

def run_agent(user_input: str) -> tuple[str, str, str, str]:
    """
    Runs TaskPlannerAgent
    Returns:
        plan, steps_result, final_output, logs
    """
    if not user_input.strip():
        return "Error", "Error", "Please enter a goal.", "No input provided."
        
    try:
        # Assuming the app is run from within the task_planner directory
        # or the root directory. We'll use the director of app.py.
        root_dir = os.path.dirname(os.path.abspath(__file__))
        
        agent = TaskPlannerAgent(root_dir=root_dir)
        plan, steps_result, final_output, logs = agent.run(user_input)
        
        return plan, steps_result, final_output, logs
    except Exception as e:
        import traceback
        err = f"An exception occurred:\n{traceback.format_exc()}"
        return "Error", "Error", "Execution Failed", err

# UI Layout
with gr.Blocks(title="Task Planner Agent") as app:
    gr.Markdown("# 🧩 Task Planner Agent")
    gr.Markdown("Enter a complex goal, and the agent will break it down, execute it sequentially using memory context, and summarize the results.")
    
    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(label="Enter your goal", placeholder="e.g., Build a startup", lines=3)
            submit_btn = gr.Button("Run Planner", variant="primary")
            
        with gr.Column():
            plan_output = gr.Textbox(label="Generated Plan", lines=6, interactive=False)
            
    with gr.Row():
        steps_output = gr.Textbox(label="Execution Results", lines=10, interactive=False)
        
    with gr.Row():
        final_output = gr.Textbox(label="Final Answer", lines=5, interactive=False)
        
    with gr.Row():
        logs_output = gr.Textbox(label="Logs", lines=12, interactive=False)

    # Event binding
    submit_btn.click(
        fn=run_agent,
        inputs=input_box,
        outputs=[
            plan_output,
            steps_output,
            final_output,
            logs_output
        ]
    )

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not found in environment. The application will fail to run the agent.")
        
    print("Starting Task Planner Agent UI...")
    app.launch()
