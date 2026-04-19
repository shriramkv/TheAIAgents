from fastapi import APIRouter, Request, HTTPException
from app.api.schemas import AgentRequest, AgentResponse, HealthResponse
from app.services.agent_service import agent_service
from app.core.monitoring import metrics_tracker

router = APIRouter()

@router.post("/run-agent", response_model=AgentResponse)
async def run_agent(request_data: AgentRequest, request: Request):
    """
    Endpoint to interact with the AI agent.
    """
    try:
        request_id = getattr(request.state, "request_id", "unknown")
        result = agent_service.run_agent(request_data.input, request_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint that returns API status and basic metrics.
    """
    return {
        "status": "ok",
        "metrics": metrics_tracker.get_metrics()
    }
