from pydantic import BaseModel, Field
from typing import Dict, Any

class AgentRequest(BaseModel):
    """
    Request schema for the agent endpoint.
    """
    input: str = Field(..., description="The user query or input for the agent.")

class AgentResponse(BaseModel):
    """
    Response schema for the agent endpoint.
    """
    response: str = Field(..., description="The final response from the agent.")
    logs: str = Field(..., description="Detailed execution logs and timing.")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata about the request.")

class HealthResponse(BaseModel):
    """
    Response schema for the health check endpoint.
    """
    status: str = "ok"
    metrics: Dict[str, Any]
