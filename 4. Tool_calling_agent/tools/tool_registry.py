from .calculator import calculator
from .datetime_tool import get_current_time
from .string_tools import reverse_string

# Centralized registry mapping
# Defines the JSON schema for each tool to be consumed by OpenAI

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g., '25 * 18'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns current system time",
            "parameters": {
                "type": "object",
                "properties": {} # No inputs required
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reverse_string",
            "description": "Reverse a string",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The string to reverse"
                    }
                },
                "required": ["text"]
            }
        }
    }
]

# Map string names of tools to the actual Python functions
TOOL_MAP = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "reverse_string": reverse_string
}

def execute_tool(tool_name: str, args_dict: dict) -> str:
    """
    Helper function to dynamically call a tool by name with arguments.
    
    Args:
        tool_name: The name of the tool to execute.
        args_dict: A dictionary of arguments to pass to the tool.
        
    Returns:
        The result of the tool execution as a string, including error messages.
    """
    if tool_name not in TOOL_MAP:
        return f"Error: Tool '{tool_name}' not found in registry."
        
    try:
        func = TOOL_MAP[tool_name]
        result = func(**args_dict)
        return str(result)
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"
