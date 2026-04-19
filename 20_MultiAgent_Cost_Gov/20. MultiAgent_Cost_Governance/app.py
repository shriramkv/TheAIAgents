import gradio as gr
import pandas as pd
import plotly.express as px
from agent import CostGovernorAgent
import os
from dotenv import load_dotenv

load_dotenv()

def run_governor(prompt, budget):
    agent = CostGovernorAgent(budget=float(budget))
    result = agent.run(prompt)
    
    # Prepare data for history table
    history_df = pd.DataFrame(result['history'])
    
    # Prepare data for plotting
    plot_data = []
    accumulated = 0
    for i, entry in enumerate(result['history']):
        accumulated += entry['cost']
        plot_data.append({
            "Step": i + 1,
            "Cost": entry['cost'],
            "Accumulated Cost": accumulated,
            "Model": entry['model']
        })
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create Plotly chart
    fig = px.line(plot_df, x="Step", y="Accumulated Cost", 
                title="Cumulative Cost vs Budget Cap",
                markers=True, text="Model")
    
    fig.add_hline(y=float(budget), line_dash="dash", line_color="red", 
                  annotation_text="Budget Cap")
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )

    decision_logs = "\n".join(result['decision_logs'])
    
    status = "✅ Completed" if result['total_cost'] < float(budget) else "⚠️ Stopped Early (Budget Exceeded)"
    
    return (
        result['response'],
        f"${result['total_cost']:.6f}",
        f"{result['tokens']}",
        status,
        history_df,
        fig,
        decision_logs
    )

# UI Design
with gr.Blocks(title="Multi-Agent Cost Governor") as demo:
    gr.Markdown("""
    # 🛡️ Multi-Agent Cost Governor
    ### Real-time Token Tracking & Adaptive Model Routing
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            budget_input = gr.Number(label="Budget Cap (USD)", value=0.005, precision=4)
            user_input = gr.Textbox(label="User Query", placeholder="Enter a complex task...", lines=3)
            submit_btn = gr.Button("🚀 Run Governor", variant="primary")
            
        with gr.Column(scale=2):
            with gr.Row():
                cost_out = gr.Label(label="Total Cost")
                token_out = gr.Label(label="Total Tokens")
                status_out = gr.Label(label="Status")
            
            output_text = gr.Textbox(label="Final Response", lines=8, interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📊 Cost Accumulation")
            cost_plot = gr.Plot()
        
        with gr.Column():
            gr.Markdown("### 📜 Decision Logs")
            logs_out = gr.Textbox(label="Trace", lines=10, interactive=False)

    with gr.Row():
        gr.Markdown("### 📋 Transaction History")
        history_table = gr.Dataframe(interactive=False)

    submit_btn.click(
        fn=run_governor,
        inputs=[user_input, budget_input],
        outputs=[output_text, cost_out, token_out, status_out, history_table, cost_plot, logs_out]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
