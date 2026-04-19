import gradio as gr
import pandas as pd
import json
from agent import AuditedAgent
from shared.utils import load_config
import os

# Initialize Agent
agent = AuditedAgent()
config = load_config()

def process_query(query):
    """
    Process user query through the agent and retrieve latest audit logs.
    """
    if not query.strip():
        return "Please enter a query.", None, []

    # Run agent
    result = agent.run(query)
    response = result["response"]
    trace_id = result["trace_id"]

    # Load all logs to find the ones for this trace
    all_logs = agent.storage.load_all()
    session_logs = [log for log in all_logs if log.get("trace_id") == trace_id]
    
    # Format logs for display
    display_logs = []
    for log in session_logs:
        display_logs.append({
            "Step": log.get("step_type"),
            "Content": log.get("content"),
            "Tool": log.get("tool") or "-",
            "Decision": log.get("decision") or "-",
            "Timestamp": log.get("timestamp").split("T")[1].split(".")[0], # HH:MM:SS
            "Trace ID": log.get("trace_id")
        })

    return response, trace_id, pd.DataFrame(display_logs)

def refresh_logs():
    """
    Load all logs from storage.
    """
    all_logs = agent.storage.load_all()
    if not all_logs:
        return pd.DataFrame()
    
    # Sort by timestamp descending
    all_logs.sort(key=lambda x: x.get("timestamp"), reverse=True)
    
    return pd.DataFrame(all_logs)

# UI Design
with gr.Blocks(theme=gr.themes.Soft(), title="Audit-Trail Agent Pipeline") as demo:
    gr.Markdown("# 🕵️‍♂️ Audit-Trail Agent Pipeline")
    gr.Markdown("An AI agent that logs every internal thought and decision for full observability.")
    
    with gr.Tab("Agent Chat"):
        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(label="Enter your query (e.g., 'What is 125 * 8?')", placeholder="Ask me something...")
                submit_btn = gr.Button("Execute Agent", variant="primary")
                
                response_output = gr.Textbox(label="Agent Response", interactive=False)
                trace_output = gr.Label(label="Trace ID")
            
            with gr.Column(scale=3):
                gr.Markdown("### 📜 Current Session Audit Trail")
                audit_table = gr.Dataframe(
                    headers=["Step", "Content", "Tool", "Decision", "Timestamp"],
                    datatype=["str", "str", "str", "str", "str"],
                    interactive=False
                )

    with gr.Tab("Full Audit History"):
        gr.Markdown("### 🗂️ Global Audit Logs")
        refresh_btn = gr.Button("Refresh History")
        full_history_table = gr.Dataframe(interactive=False)
        
        refresh_btn.click(fn=refresh_logs, outputs=full_history_table)

    # Interactivity
    submit_btn.click(
        fn=process_query,
        inputs=query_input,
        outputs=[response_output, trace_output, audit_table]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
