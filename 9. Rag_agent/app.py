import gradio as gr
from agent import RAGAgent

# Initialize the RAG Agent
agent = RAGAgent()

def run_agent(user_input: str, file) -> tuple:
    """
    Handles optional ingestion and query processing.

    Args:
        user_input (str): The user's question.
        file (tempfile._TemporaryFileWrapper): Optional file uploaded by the user.

    Returns:
        tuple: Retrieved context, final answer, logs.
    """
    logs_accumulator = ""

    # Check if a document is uploaded and ingest it
    if file is not None:
        file_path = file.name
        logs_accumulator += f"Starting ingestion for uploaded file: {file_path}\\n"
        success = agent.ingest_document(file_path)
        if success:
            logs_accumulator += "File ingestion completed successfully.\\n\\n"
        else:
            logs_accumulator += "File ingestion failed. Check backend logs.\\n\\n"

    # Ensure there's a query before processing
    if not user_input.strip():
        return "", "Please ask a valid question.", logs_accumulator + "No query provided."

    # Run the query against the logic
    context, answer, agent_logs = agent.run(user_input)
    
    # Compile the final logs display
    final_logs = logs_accumulator + agent_logs

    return context, answer, final_logs

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📚 Agentic RAG Assistant")
    gr.Markdown("Upload a document (`.txt` or `.pdf`) to add to the knowledge base, then ask a question grounded in the text.")

    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(label="Upload Document (optional)", file_types=[".txt", ".pdf"])
            input_box = gr.Textbox(label="Ask a question", placeholder="e.g., What is water quality management?")
            submit_btn = gr.Button("Run RAG", variant="primary")
            
        with gr.Column(scale=2):
            answer_output = gr.Textbox(label="Final Answer", lines=5)
            context_output = gr.Textbox(label="Retrieved Context", lines=8)
            logs_output = gr.Textbox(label="Logs", lines=12)

    submit_btn.click(
        fn=run_agent,
        inputs=[input_box, file_upload],
        outputs=[context_output, answer_output, logs_output]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
