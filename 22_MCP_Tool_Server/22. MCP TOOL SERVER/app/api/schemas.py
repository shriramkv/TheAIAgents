from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

class ToolDiscoveryResponse(BaseModel):
    tools: List[ToolDefinition]

class ToolExecutionRequest(BaseModel):
    parameters: Dict[str, Any] = Field(..., description="The parameters required by the tool.")

class ToolExecutionResponse(BaseModel):
    result: Optional[Any] = None
    error: Optional[str] = None
