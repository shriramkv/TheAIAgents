import time
from typing import Any, Dict, Optional
from app.tools.tool_registry import get_tool_function, get_tool_metadata
from app.core.logger import log_tool_call

class ToolService:
    """
    Service layer for discovering and executing MCP tools.
    """
    
    def discover_tools(self) -> Dict[str, Any]:
        """
        Returns all registered tools and their schemas.
        """
        return {
            "tools": get_tool_metadata()
        }

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finds a tool in the registry, executes it safely, and logs the result.
        """
        tool_func = get_tool_function(tool_name)
        
        if not tool_func:
            return {"error": f"Tool '{tool_name}' not found."}
        
        start_time = time.perf_counter()
        try:
            # Execute the tool
            result = tool_func(**parameters)
            duration = time.perf_counter() - start_time
            
            # Log the execution
            log_tool_call(tool_name, parameters, result, duration)
            
            return {"result": result}
            
        except TypeError as e:
            return {"error": f"Invalid parameters for tool '{tool_name}': {str(e)}"}
        except Exception as e:
            return {"error": f"Execution failed for tool '{tool_name}': {str(e)}"}

tool_service = ToolService()
