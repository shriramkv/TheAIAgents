from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.logger import LoggingMiddleware
from app.core.config import settings

def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Dockerized Agent API",
        description="A production-ready API wrapper for an AI agent.",
        version="1.0.0",
        debug=settings.DEBUG
    )

    # Add middlewarres
    app.add_middleware(LoggingMiddleware)

    # Include routers
    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
