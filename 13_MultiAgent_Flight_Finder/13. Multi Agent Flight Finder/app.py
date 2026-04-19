import gradio as gr
import json
from agent import FlightFinderAgent

# Initialize the agent
agent = FlightFinderAgent()

def find_flights_ui(origin, destination, date, budget, layovers):
    """
    Wrapper for the Gradio UI to call the agent.
    """
    try:
        result = agent.find_flights(origin, destination, date, budget, layovers)
        
        all_flights_str = json.dumps(result["all_flights"], indent=2)
        filtered_flights_str = json.dumps(result["filtered_flights"], indent=2)
        best_flight_str = json.dumps(result["best_flight"], indent=2) if result["best_flight"] else "None"
        
        return (
            all_flights_str,
            filtered_flights_str,
            best_flight_str,
            result["explanation"],
            result["logs"]
        )
    except Exception as e:
        return f"Error: {str(e)}", "", "", "", f"Error occurred: {str(e)}"

# Define Gradio Layout
with gr.Blocks(title="✈️ Multi-Agent Flight Finder") as app:
    gr.Markdown("# ✈️ Multi-Agent Flight Finder")
    gr.Markdown("Find the best flights using specialized AI agents.")
    
    with gr.Row():
        with gr.Column():
            origin = gr.Textbox(label="Origin (e.g., BLR)", value="BLR")
            destination = gr.Textbox(label="Destination (e.g., DEL)", value="DEL")
            date = gr.Textbox(label="Date (e.g., 2024-12-01)", value="2024-12-01")
            
            budget = gr.Number(label="Budget (₹)", value=10000)
            layovers = gr.Number(label="Max Layovers", value=1)
            
            submit_btn = gr.Button("Find My Flight", variant="primary")
            
        with gr.Column():
            best_flight = gr.Textbox(label="Best Flight Selection", lines=3)
            explanation = gr.Textbox(label="Agent Reasoning", lines=5)

    with gr.Tabs():
        with gr.TabItem("Search Logs"):
            logs = gr.Textbox(label="System Logs", lines=20)
        with gr.TabItem("All Flights"):
            all_flights = gr.Textbox(label="All Found Flights", lines=20)
        with gr.TabItem("Filtered Flights"):
            filtered_flights = gr.Textbox(label="Validated Flights", lines=20)

    # Connect components
    submit_btn.click(
        fn=find_flights_ui,
        inputs=[origin, destination, date, budget, layovers],
        outputs=[all_flights, filtered_flights, best_flight, explanation, logs]
    )

if __name__ == "__main__":
    app.launch()
