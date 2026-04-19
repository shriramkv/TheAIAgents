# app.py
import gradio as gr
from ui.controller import start_interview, submit_answer, end_interview, ROLES, DIFFICULTIES

def build_ui():
    """
    Construct the Gradio User Interface.
    """
    with gr.Blocks(title="Interview Practice Partner") as demo:
        gr.Markdown("# 🤖 Interview Practice Partner")
        gr.Markdown("Practice your interview skills with an AI coach. Upload your resume, speak your answers, and get detailed feedback.")
        
        with gr.Row():
            with gr.Column(scale=1):
                role = gr.Dropdown(choices=ROLES, value="software_engineer", label="Target Role")
                diff = gr.Dropdown(choices=DIFFICULTIES, value="medium", label="Difficulty Level")
                resume = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
                start = gr.Button("🚀 Start Interview", variant="primary")
            
            with gr.Column(scale=2):
                chat = gr.Chatbot(label="Interview Session", height=400)
        
        with gr.Row():
            with gr.Column(scale=4):
                user_input = gr.Textbox(placeholder="Type your answer here...", lines=3, label="Text Answer")
            with gr.Column(scale=1):
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Voice Answer")
        
        with gr.Row():
            send = gr.Button("Submit Answer", variant="primary")
            end = gr.Button("End Interview & Get Report", variant="secondary")
            
        with gr.Row():
            audio_output = gr.Audio(label="Agent Voice", autoplay=True, visible=False) # Hidden audio player for auto-play
            
        with gr.Accordion("Real-time Feedback", open=False):
            feedback = gr.Textbox(label="Feedback on last answer", lines=4)
            
        report_display = gr.Markdown(label="Final Report")
        
        # State to hold the interview session data
        state = gr.State()

        # Event Handlers
        start.click(fn=start_interview, inputs=[role, diff, resume], outputs=[chat, state])
        send.click(fn=submit_answer, inputs=[state, user_input, audio_input, chat], outputs=[feedback, chat, state, user_input, audio_output])
        end.click(fn=end_interview, inputs=[state], outputs=[report_display])

    return demo

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(share=False)
