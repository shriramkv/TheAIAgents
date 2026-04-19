import gradio as gr
from agent import VoiceRAGAgent
from shared.logger import get_ui_logs, clear_ui_logs
from ingestion.indexer import build_index
import os

# Initialize agent
agent = VoiceRAGAgent()

def run_agent(audio_file):
    """
    Returns:
    transcript,
    context,
    answer,
    audio_file_path,
    logs
    """
    if audio_file is None:
        return "", "", "Please provide audio input.", None, "No audio provided."

    # Clear previous logs
    clear_ui_logs()
    
    # Run agent
    transcript, context_chunks, answer, audio_output_path = agent.run(audio_file)
    
    # Format context for display
    context_display = "\n\n---\n\n".join(context_chunks)
    
    # Get logs from buffer
    logs = get_ui_logs()
    
    return transcript, context_display, answer, audio_output_path, logs

# Build the Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎤 Voice RAG Agent")
    gr.Markdown("Speak into your microphone or upload an audio file to query the knowledge base.")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(type="filepath", label="Speak or Upload Audio")
            submit_btn = gr.Button("Run Voice Agent", variant="primary")
        
        with gr.Column():
            audio_output = gr.Audio(label="Audio Response")

    with gr.Tabs():
        with gr.TabItem("Results"):
            transcript_output = gr.Textbox(label="Transcript")
            answer_output = gr.Textbox(label="Answer")
        
        with gr.TabItem("Context"):
            context_output = gr.Textbox(label="Retrieved Context", lines=10)
        
        with gr.TabItem("Logs"):
            logs_output = gr.Textbox(label="Logs", lines=12)

    submit_btn.click(
        fn=run_agent,
        inputs=audio_input,
        outputs=[
            transcript_output,
            context_output,
            answer_output,
            audio_output,
            logs_output
        ]
    )

if __name__ == "__main__":
    # Ensure sample docs exist for demonstration
    os.makedirs("data/sample_docs", exist_ok=True)
    sample_file = "data/sample_docs/knowledge.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write("Water quality monitoring is the process of sampling and analyzing water to estimate its quality. It is essential for protecting aquatic life and human health.")
            f.write("\n\nAeroponics is a plant-cultivation technique in which the roots hang suspended in the air while nutrient-enriched water is sprayed on them.")
    
    # Build index if it doesn't exist
    if not os.path.exists("vectorstore.index"):
        print("Building initial index...")
        build_index()

    app.launch()
