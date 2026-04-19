import time
import threading
from typing import Optional, Dict
from shared.logger import logger
from shared.utils import load_config

# Global approval state for local simulation (e.g. via UI)
approval_store: Dict[str, Optional[bool]] = {}

class ApprovalHandler:
    def __init__(self):
        self.config = load_config()
        self.timeout = self.config.get("approval_timeout", 60)

    def wait_for_approval(self, request_id: str) -> bool:
        """
        Wait for human response:
        - APPROVED → True
        - REJECTED → False
        - TIMEOUT → False
        """
        logger.info(f"Waiting for approval (Request ID: {request_id}, Timeout: {self.timeout}s)...")
        
        # Initialize the request in the store
        approval_store[request_id] = None
        
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            # Check if the state has been updated (e.g., from the UI or external webhook)
            status = approval_store.get(request_id)
            if status is not None:
                logger.log_approval_status(status)
                return status
            
            # For demonstration, in CLI mode if no UI is provided, 
            # we might want to check for a file or just wait.
            # Here we just sleep and poll.
            time.sleep(1)
        
        logger.error(f"Approval timed out after {self.timeout} seconds.")
        logger.log_approval_status(False)
        return False

    def provide_response(self, request_id: str, approved: bool):
        """
        Allows external entities (like Gradio UI) to provide a response.
        """
        approval_store[request_id] = approved
        logger.info(f"Response provided for {request_id}: {'APPROVED' if approved else 'REJECTED'}")

approval_handler = ApprovalHandler()
