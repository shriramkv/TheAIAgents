import gradio as gr
import json
from agent import FinancialAnalystAgent
from shared.utils import load_config
from shared.logger import logger

# Initialize Agent
agent = FinancialAnalystAgent()
config = load_config()

def analyze_ticker(ticker: str):
    """
    Main UI handler function.
    """
    if not ticker:
        return "Please enter a ticker", "", "", "", "Error: No ticker provided"
    
    try:
        # Run the agent pipeline
        result = agent.run(ticker.upper())
        
        # Format outputs for Gradio
        stock_data_str = json.dumps(result["stock_data"], indent=2)
        ratios_str = json.dumps(result["ratios"], indent=2)
        
        # Format news
        news_list = result["news"]
        news_str = ""
        for n in news_list:
            news_str += f"Title: {n['title']}\nSummary: {n['summary']}\nURL: {n['url']}\n\n"
        
        return (
            stock_data_str,
            ratios_str,
            news_str,
            result["memo"],
            result["logs"]
        )
    except Exception as e:
        logger.error(f"UI Error: {e}")
        return "Error", "Error", "Error", f"An error occurred: {str(e)}", "Error"

# Build UI
with gr.Blocks(title="Financial Analyst Agent", theme=gr.themes.Soft()) as app:
    gr.Markdown(f"# {config.get('app_title', '📊 Financial Analyst Agent')}")
    gr.Markdown("Enter a stock ticker symbol (e.g., AAPL, TSLA, GOOGL) to generate a professional investment memo.")
    
    with gr.Row():
        with gr.Column(scale=1):
            ticker_input = gr.Textbox(label="Stock Ticker", placeholder="e.g. AAPL")
            submit_btn = gr.Button("Analyze Stock", variant="primary")
            
        with gr.Column(scale=2):
            logs_output = gr.Textbox(label="Agent Reasoning Logs", lines=10)

    with gr.Tabs():
        with gr.Tab("Investment Memo"):
            memo_output = gr.Markdown(label="Final Memo")
            
        with gr.Tab("Financial Data"):
            with gr.Row():
                stock_output = gr.Code(label="Stock Metrics", language="json")
                ratios_output = gr.Code(label="Key Ratios", language="json")
                
        with gr.Tab("Recent News"):
            news_output = gr.Textbox(label="Latest Headlines", lines=15)

    # Wire up events
    submit_btn.click(
        fn=analyze_ticker,
        inputs=[ticker_input],
        outputs=[stock_output, ratios_output, news_output, memo_output, logs_output]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
