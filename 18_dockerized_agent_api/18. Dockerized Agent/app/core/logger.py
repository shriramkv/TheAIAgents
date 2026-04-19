import logging
import time
import sys
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("agent_api")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log request details and execution time.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        # Log Request Start
        logger.info(f"[{request_id}] START {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time
            
            # Log Request End
            logger.info(
                f"[{request_id}] END {request.method} {request.url.path} "
                f"- Status: {response.status_code} - Time: {process_time:.4f}s"
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] FAILED {request.method} {request.url.path} "
                f"- Error: {str(e)} - Time: {process_time:.4f}s"
            )
            raise e
