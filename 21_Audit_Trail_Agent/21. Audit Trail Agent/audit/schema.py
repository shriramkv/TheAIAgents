from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class AuditStep(BaseModel):
    """
    Schema for a single step in the agent's audit trail.
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    agent_name: str
    step_type: str  # thought/action/observation/decision
    content: str
    tool: Optional[str] = None
    decision: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": "2024-04-18T21:00:00Z",
                "agent_name": "AuditedAgent",
                "step_type": "thought",
                "content": "I need to calculate the sum of 2 and 2",
                "tool": "calculator",
                "decision": "proceed",
                "metadata": {"tokens_used": 150, "latency": 0.5}
            }
        }
