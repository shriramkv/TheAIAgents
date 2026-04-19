import gradio as gr
from agent import WebResearchAgent
from typing import Tuple

# Initialize the agent
agent = WebResearchAgent()

def run_research(topic: str) -> Tuple[str, str, str]:
    """
    Wrapper function for the Gradio interface.
    """
    if not topic.strip():
        return "Please enter a valid research topic.", "", "Topic cannot be empty."
    
    report, sources, logs = agent.run(topic)
    
    # Format sources as a bulleted list for display
    sources_text = "\n".join([f"- {url}" for url in sources]) if sources else "No sources found."
    
    return report, sources_text, logs

def create_ui():
    """
    Defines the Gradio UI layout and behavior.
    """
    with gr.Blocks(title="Web Research Summarizer Agent") as demo:
        gr.Markdown("# 🌐 Web Research Summarizer Agent")
        gr.Markdown("Enter a research topic, and the agent will expand the query, search the web, scrape content, and synthesize a summarized report.")
        
        with gr.Row():
            with gr.Column(scale=4):
                input_box = gr.Textbox(
                    label="Enter research topic", 
                    placeholder="e.g., Latest trends in AI agents 2024",
                    lines=2
                )
                submit_btn = gr.Button("Run Research", variant="primary")
            
        with gr.Tabs():
            with gr.TabItem("Research Report"):
                report_output = gr.Markdown(label="Final Report")
            with gr.TabItem("Sources"):
                sources_output = gr.Textbox(label="Sources Used", lines=5)
            with gr.TabItem("Reasoning Logs"):
                logs_output = gr.Code(label="Agent Trace", language="markdown", lines=15)
        
        # Define interaction
        submit_btn.click(
            fn=run_research,
            inputs=[input_box],
            outputs=[report_output, sources_output, logs_output]
        )

    return demo

if __name__ == "__main__":
    app = create_ui()
    app.launch()
