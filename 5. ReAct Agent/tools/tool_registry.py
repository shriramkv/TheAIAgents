from tools.calculator import calculator
from tools.search_mock import search

class ToolRegistry:
    def __init__(self):
        # Map string names to practical functions
        self.tools = {
            "calculator": calculator,
            "search": search
        }
        
    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """
        Executes a registered tool dynamically.
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}."
            
        try:
            func = self.tools[tool_name]
            result = func(tool_input)
            return str(result)
        except Exception as e:
            return f"Error during tool execution: {e}"
            
    def get_tool_descriptions(self) -> str:
        """
        Provides documentation of all tools for the prompt
        """
        return (
            "- `calculator`: Safely evaluate math expressions. Input should be a mathematical string like '25 * 4'.\n"
            "- `search`: Useful for getting general real-time information or lookups. Input should be a search query."
        )
