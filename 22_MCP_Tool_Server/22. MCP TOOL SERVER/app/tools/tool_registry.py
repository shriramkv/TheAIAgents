from typing import Dict, Any, List, Callable
from app.tools.crm_tool import get_customer_info
from app.tools.db_tool import query_internal_db

# Tool definitions in MCP-compatible format
TOOLS_MANIFEST: List[Dict[str, Any]] = [
    {
        "name": "get_customer_info",
        "description": "Retrieve comprehensive customer details from the internal CRM database using a customer ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The unique ID of the customer (e.g., CUST-001)."
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "query_internal_db",
        "description": "Execute natural language or keyword-based queries against internal inventory and revenue data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The natural language query (e.g., 'Check inventory for laptops')."
                }
            },
            "required": ["query"]
        }
    }
]

# Mapping tool names to execution functions
TOOL_MAP: Dict[str, Callable] = {
    "get_customer_info": get_customer_info,
    "query_internal_db": query_internal_db
}

def get_tool_metadata() -> List[Dict[str, Any]]:
    """Returns the list of available tools and their schemas."""
    return TOOLS_MANIFEST

def get_tool_function(tool_name: str) -> Callable:
    """Retrieves the function associated with a tool name."""
    return TOOL_MAP.get(tool_name)
