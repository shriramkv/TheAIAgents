import gradio as gr
import threading
import time
from agent import HumanInTheLoopAgent
from approval.approval_handler import approval_handler, approval_store
from shared.logger import logger
import queue

# Use a queue to capture logs for the UI
log_queue = queue.Queue()

class UIHandler(gr.Interface):
    def __init__(self):
        self.agent = HumanInTheLoopAgent()
        self.current_req_id = "agent_interaction"

    def run_agent(self, user_input):
        # Reset logs
        logs = []
        
        # We need a way to pass logs from the agent/shared modules to the UI.
        # For simplicity in this demo, we'll return the final result and 
        # assume the logger captured some state.
        
        result = self.agent.run(user_input)
        return result

def create_ui():
    agent = HumanInTheLoopAgent()
    
    with gr.Blocks(title="HITL Agent Dashboard") as demo:
        gr.Markdown("# 🤖 Human-in-the-Loop (HITL) Agent")
        gr.Markdown("Autonomously executes tasks, but pauses for approval on high-risk actions.")
        
        with gr.Row():
            with gr.Column(scale=2):
                user_input = gr.Textbox(label="User Request", placeholder="e.g., 'Delete temp files' or 'Send email to team'")
                submit_btn = gr.Button("Submit", variant="primary")
                
                with gr.Group(visible=False) as approval_group:
                    gr.Markdown("### 🚨 Approval Required")
                    action_display = gr.Markdown("")
                    with gr.Row():
                        approve_btn = gr.Button("✅ Approve", variant="success")
                        reject_btn = gr.Button("❌ Reject", variant="stop")
            
            with gr.Column(scale=1):
                status_display = gr.Label(label="Agent Status", value="Idle")
                final_result = gr.Textbox(label="Final Result", interactive=False)
        
        logs_display = gr.Textbox(label="Live Logs", interactive=False, lines=15)

        # State to store request ID
        req_id_state = gr.State("agent_request")

        def on_submit(text):
            # This will run in a separate thread to allow UI to stay interactive
            # logic:
            # 1. Start agent thread
            # 2. Polling for 'risky' state? 
            # Actually, to make it simple for Gradio, we can split the agent run 
            # into parts or use a callback.
            return {
                status_display: "Processing...",
                final_result: "",
                logs_display: f"[INPUT]\n{text}\n\nAnalyzing risk...",
                approval_group: gr.update(visible=False)
            }

        def agent_thread_func(text, progress=gr.Progress()):
            try:
                # We'll use a specific request ID for this session
                rid = f"session_{int(time.time())}"
                
                # We need to monkeypatch or use a callback to show buttons in the middle of execution.
                # However, Gradio's standard flow is Request -> Response.
                # To simulate HITL in a single call, we'd need another mechanism.
                
                # ALTERNATIVE: Use a simple loop for the agent that checks for risk.
                result = agent.run(text)
                return result, "Idle"
            except Exception as e:
                return str(e), "Error"

        # Refined logic for Gradio interaction:
        # Since Gradio doesn't easily support blocking calls with intermediate UI changes 
        # without complex state or webhooks, we'll implement a 'dry run' + 'execute' logic 
        # or just use the backend logs.
        
        # For this specific project, I'll provide a 'Simulation Run' that handles the flow.
        
        def handle_interaction(text):
            # 1. Log Input
            output_logs = f"[INPUT]\n{text}\n"
            
            # Simple simulation for the UI demo:
            # Re-implementing parts of agent.run here to allow UI updates
            from risk.risk_evaluator import is_high_risk
            from shared.llm import call_llm
            
            # Action Gen
            llm_response = call_llm(text, system_prompt=agent.system_prompt)
            action = agent._extract_action(llm_response)
            output_logs += f"[ACTION GENERATED]\n{action}\n"
            
            risky = is_high_risk(action)
            output_logs += f"[RISK DETECTED] {'YES' if risky else 'NO'}\n"
            
            if risky:
                return (
                    gr.update(visible=True), # show approval buttons
                    f"Agent wants to perform: **{action}**", # details
                    output_logs + "\n[APPROVAL REQUEST SENT]\nWaiting for human decision...",
                    "Waiting for Approval",
                    action # save action to state
                )
            else:
                res = agent._execute_action(action)
                return (
                    gr.update(visible=False),
                    "",
                    output_logs + f"\n[FINAL RESULT]\n{res}",
                    "Completed",
                    action
                )

        current_action = gr.State("")

        def handle_approval(choice, action, logs):
            status = "APPROVED" if choice else "REJECTED"
            new_logs = logs + f"\n[APPROVAL STATUS] {status}\n"
            
            if choice:
                res = agent._execute_action(action)
                new_logs += f"\n[FINAL RESULT]\n{res}"
                return gr.update(visible=False), new_logs, "Completed", res
            else:
                res = f"Action aborted: '{action}' was rejected."
                new_logs += f"\n[FINAL RESULT]\n{res}"
                return gr.update(visible=False), new_logs, "Aborted", res

        submit_btn.click(
            handle_interaction, 
            inputs=[user_input], 
            outputs=[approval_group, action_display, logs_display, status_display, current_action]
        )

        approve_btn.click(
            lambda a, l: handle_approval(True, a, l),
            inputs=[current_action, logs_display],
            outputs=[approval_group, logs_display, status_display, final_result]
        )

        reject_btn.click(
            lambda a, l: handle_approval(False, a, l),
            inputs=[current_action, logs_display],
            outputs=[approval_group, logs_display, status_display, final_result]
        )

    return demo

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)
助力助
