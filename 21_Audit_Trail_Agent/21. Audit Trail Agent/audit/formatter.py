from datetime import datetime
from typing import Optional, Dict, Any
from .schema import AuditStep

def format_step(
    agent_name: str,
    step_type: str,
    content: str,
    trace_id: str,
    tool: Optional[str] = None,
    decision: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Format a step into the standardized audit schema.
    
    Args:
        agent_name: Name of the agent performing the step
        step_type: Type of step (thought/action/observation/decision)
        content: The core content of the step
        trace_id: Unique identifier for the trace
        tool: Optional tool used in this step
        decision: Optional decision made in this step
        metadata: Optional dictionary of additional metadata (e.g. tokens, latency)
        
    Returns:
        A dictionary representation of the AuditStep
    """
    step = AuditStep(
        trace_id=trace_id,
        timestamp=datetime.now().isoformat(),
        agent_name=agent_name,
        step_type=step_type,
        content=content,
        tool=tool,
        decision=decision,
        metadata=metadata or {}
    )
    return step.model_dump()
