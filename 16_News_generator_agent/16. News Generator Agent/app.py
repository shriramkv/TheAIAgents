import gradio as gr
from agent import NewsGeneratorAgent
from shared.logger import logger

def run_agent(category, tone, length):
    """
    Interface function to connect Gradio to the NewsGeneratorAgent.
    """
    logger.info("Initializing News Generator Agent run...")
    agent = NewsGeneratorAgent()
    newsletter, logs = agent.run(category, tone, length)
    return newsletter, logs

# Define UI
with gr.Blocks() as app:
    gr.Markdown("# 📰 News Generator Agent")
    gr.Markdown("Aggregate, cluster, and summarize news into a professional newsletter.")

    with gr.Row():
        with gr.Column(scale=1):
            category = gr.Dropdown(
                ["All", "Tech", "Finance", "World"], 
                label="Category", 
                value="Tech"
            )
            tone = gr.Dropdown(
                ["Formal", "Casual", "Gen Z", "Professional"], 
                label="Tone", 
                value="Formal"
            )
            length = gr.Dropdown(
                ["Short", "Medium", "Long"], 
                label="Length", 
                value="Medium"
            )
            submit_btn = gr.Button("Generate Newsletter", variant="primary")

        with gr.Column(scale=2):
            newsletter_output = gr.Textbox(
                label="Newsletter Output", 
                lines=20
            )
            
    with gr.Row():
        logs_output = gr.Textbox(
            label="Agent Reasoning Logs", 
            lines=10, 
            interactive=False
        )

    submit_btn.click(
        fn=run_agent,
        inputs=[category, tone, length],
        outputs=[newsletter_output, logs_output]
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
