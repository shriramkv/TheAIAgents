from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas import ToolDiscoveryResponse, ToolExecutionRequest, ToolExecutionResponse
from app.services.tool_service import tool_service
from app.core.auth import verify_api_key

router = APIRouter()

@router.get(
    "/tools",
    response_model=ToolDiscoveryResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Discover available tools",
    description="Returns a list of all MCP-compatible tools registered on the server."
)
async def get_tools():
    """Returns the tool manifest."""
    return tool_service.discover_tools()

@router.post(
    "/tools/{tool_name}",
    response_model=ToolExecutionResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Execute a tool",
    description="Executes a specific tool by name with the provided parameters."
)
async def call_tool(tool_name: str, request: ToolExecutionRequest):
    """Executes a tool and returns the result."""
    response = tool_service.execute_tool(tool_name, request.parameters)
    
    if "error" in response:
        # We still return 200 but include error in the body as per some tool protocol styles,
        # or we could raise a 400. Here we follow the requested schema return.
        return ToolExecutionResponse(error=response["error"])
        
    return ToolExecutionResponse(result=response["result"])
