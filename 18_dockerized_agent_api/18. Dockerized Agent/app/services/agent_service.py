import time
from typing import Dict, Any
from app.agents.sample_agent import SampleAgent
from app.utils.helpers import format_agent_logs, get_timestamp
from app.core.monitoring import metrics_tracker
from app.core.logger import logger

class AgentService:
    """
    Service layer to handle agent execution, logging, and metrics.
    """
    def __init__(self):
        self.agent = SampleAgent()

    def run_agent(self, user_input: str, request_id: str) -> Dict[str, Any]:
        """
        Orchestrates the agent run, calculates execution time, and updates metrics.
        """
        start_time = time.time()
        metrics_tracker.track_request()
        
        try:
            # Run the agent
            response_text = self.agent.run(user_input)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Update metrics
            metrics_tracker.track_latency(execution_time)
            
            # Format detailed logs for the response
            formatted_logs = format_agent_logs(user_input, response_text, execution_time)
            
            # Log structured data internally
            logger.info(f"[{request_id}] AGENT_RUN_SUCCESS - ExecTime: {execution_time:.4f}s")
            
            return {
                "response": response_text,
                "logs": formatted_logs,
                "metadata": {
                    "request_id": request_id,
                    "timestamp": get_timestamp(),
                    "execution_time": f"{execution_time:.4f}s"
                }
            }
        except Exception as e:
            metrics_tracker.track_error()
            logger.error(f"[{request_id}] AGENT_RUN_FAILED - Error: {str(e)}")
            raise e

agent_service = AgentService()
