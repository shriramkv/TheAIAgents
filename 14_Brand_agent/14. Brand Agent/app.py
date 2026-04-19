import gradio as gr
from agent import BrandMonitoringAgent
import json

def run_monitoring(brand_name: str):
    if not brand_name:
        return "Please enter a brand name.", "", "", "", "No input provided."
    
    agent = BrandMonitoringAgent()
    try:
        results = agent.run(brand_name)
        
        # Format posts for display
        post_display = ""
        for p in results["posts"]:
            post_display += f"[{p['platform'].upper()}] {p['user']}: {p['cleaned_text']} (Sentiment: {p['sentiment']})\n\n"
        
        if not post_display:
            post_display = "No posts found for this keyword."
            
        return (
            post_display,
            results["sentiment_summary"],
            results["anomaly_detection"],
            results["final_report"],
            results["logs"]
        )
    except Exception as e:
        return f"Error: {str(e)}", "N/A", "N/A", "Error occurred during analysis.", f"Logs:\n{str(e)}"

# Custom Theme and UI
with gr.Blocks(title="Brand Monitoring Agent", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📡 Brand Monitoring Agent")
    gr.Markdown("Monitor social media mentions, analyze sentiment, and detect anomalies in real-time.")
    
    with gr.Row():
        input_box = gr.Textbox(label="Enter brand name (e.g., Tesla)", placeholder="Tesla, Apple, Nike...", scale=4)
        submit_btn = gr.Button("Run Monitoring", variant="primary", scale=1)

    with gr.Tabs():
        with gr.TabItem("Analysis Report"):
            report_output = gr.Markdown(label="Final Report")
        
        with gr.TabItem("Raw Mentions"):
            posts_output = gr.Textbox(label="Collected Posts", lines=15, interactive=False)
            
        with gr.TabItem("Metrics"):
            with gr.Row():
                sentiment_output = gr.Textbox(label="Sentiment Breakdown", interactive=False)
                anomaly_output = gr.Textbox(label="Anomaly Detection", interactive=False)
        
        with gr.TabItem("System Logs"):
            logs_output = gr.Code(label="Agent Trace", language="python", lines=15)

    submit_btn.click(
        fn=run_monitoring,
        inputs=[input_box],
        outputs=[posts_output, sentiment_output, anomaly_output, report_output, logs_output]
    )

    gr.Markdown("---")
    gr.Markdown("Built with ⚡ Gradio & OpenAI (gpt-4o-mini)")

if __name__ == "__main__":
    app.launch()
