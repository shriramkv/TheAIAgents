from typing import Optional, Dict, Any
from .formatter import format_step
from .storage import AuditStorage

class AuditLogger:
    """
    Central logging class for the Audit-Trail Agent.
    Orchestrates formatting and storage of agent steps.
    """
    def __init__(self, storage: AuditStorage):
        self.storage = storage

    def log_step(
        self,
        agent_name: str,
        step_type: str,
        content: str,
        trace_id: str,
        tool: Optional[str] = None,
        decision: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log an agent step. Formats the data and saves it to persistent storage.
        """
        log_entry = format_step(
            agent_name=agent_name,
            step_type=step_type,
            content=content,
            trace_id=trace_id,
            tool=tool,
            decision=decision,
            metadata=metadata
        )
        self.storage.save(log_entry)
        return log_entry
