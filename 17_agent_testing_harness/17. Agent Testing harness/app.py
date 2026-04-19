import gradio as gr
import yaml
import json
import os
import pandas as pd
from typing import List, Dict, Any

from harness.test_runner import TestRunner
from harness.test_case import TestCase
from agent_adapters.base_adapter import AgentAdapter
from shared.utils import load_yaml
from harness.mock_tools import MOCK_TOOLS

# --- Mock Agent Implementation for Demo ---

class MockAgent(AgentAdapter):
    """
    A simple mock agent that uses the mock tools to answer questions.
    Demonstrates how to implement an adapter.
    """
    def __init__(self):
        self.tools = MOCK_TOOLS
        self.history = []

    def inject_tools(self, tools: Dict[str, Any]):
        """Harness can inject wrapped tools here."""
        self.tools = tools

    def run(self, prompt: str) -> Dict[str, Any]:
        steps = []
        output = "I don't know the answer."
        
        # Simple simulation of agent logic
        prompt_lower = prompt.lower()
        
        if " * " in prompt_lower or "+" in prompt_lower:
            # Simulate tool call
            action = "calculator"
            input_val = prompt.replace("what is", "").replace("?", "").strip()
            tool_output = self.tools["calculator"](input_val)
            steps.append(self._format_step(action, input_val, tool_output))
            output = f"The result is {tool_output}."
        
        elif "capital of" in prompt_lower:
            action = "web_search"
            input_val = prompt_lower.replace("what is the", "").strip()
            tool_output = self.tools["web_search"](input_val)
            steps.append(self._format_step(action, input_val, tool_output))
            output = f"The capital is {tool_output}."
            
        elif "weather" in prompt_lower:
            action = "get_weather"
            input_val = "London"
            tool_output = self.tools["get_weather"](input_val)
            steps.append(self._format_step(action, input_val, tool_output))
            output = f"Current weather: {tool_output}."

        # Mock metadata
        metadata = {
            "usage": {
                "total_tokens": 150 + len(steps) * 50,
                "prompt_tokens": 100,
                "completion_tokens": 50
            }
        }

        return {
            "output": output,
            "steps": steps,
            "metadata": metadata
        }

# --- UI Logic ---

def run_harness_tests(test_file):
    if test_file is None:
        return "Please upload a test file (YAML/JSON).", None, None
    
    try:
        # Load config
        config = load_yaml("config.yaml") if os.path.exists("config.yaml") else {}
        
        # Load tests
        if test_file.name.endswith(".yaml") or test_file.name.endswith(".yml"):
            raw_tests = load_yaml(test_file.name)
        else:
            with open(test_file.name, 'r') as f:
                raw_tests = json.load(f)
        
        test_cases = [TestCase.from_dict(t) for t in raw_tests]
        
        # Initialize runner and agent
        runner = TestRunner(config)
        agent = MockAgent()
        
        # Run tests
        report = runner.run_all(agent, test_cases)
        
        # Prepare table data
        results_df = pd.DataFrame(report["results"])
        
        summary_text = (
            f"### Test Summary\n"
            f"- **Total Tests:** {report['total_tests']}\n"
            f"- **Passed:** {report['passed']} ✅\n"
            f"- **Failed:** {report['failed']} ❌\n"
            f"- **Errors:** {report['errors']} ⚠️\n"
            f"- **Duration:** {report['total_duration_sec']}s"
        )
        
        return summary_text, results_df, json.dumps(report, indent=2)

    except Exception as e:
        return f"Error: {str(e)}", None, None

# --- Gradio App ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ Agent Testing Harness")
    gr.Markdown("Upload your test cases to validate agent reliability, detect loops, and track costs.")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Test File (YAML/JSON)")
            run_btn = gr.Button("🚀 Run All Tests", variant="primary")
            
        with gr.Column(scale=2):
            summary_output = gr.Markdown()
    
    with gr.Tabs():
        with gr.TabItem("📊 Results Table"):
            results_table = gr.Dataframe()
        with gr.TabItem("📜 Raw JSON Report"):
            report_json = gr.Code(language="json")
        with gr.TabItem("⚙️ Config Viewer"):
            if os.path.exists("config.yaml"):
                with open("config.yaml", 'r') as f:
                    gr.Code(f.read(), language="yaml")
    
    run_btn.click(
        fn=run_harness_tests,
        inputs=[file_input],
        outputs=[summary_output, results_table, report_json]
    )

if __name__ == "__main__":
    demo.launch(server_port=7863)
