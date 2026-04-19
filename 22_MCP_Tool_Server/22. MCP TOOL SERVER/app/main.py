from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
import logging

def create_app() -> FastAPI:
    """
    Initializes the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="A production-quality Model Context Protocol (MCP) Tool Server.",
        debug=settings.DEBUG
    )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["Health"])
    async def root():
        """Health check endpoint."""
        return {
            "status": "online",
            "app_name": settings.APP_NAME,
            "version": "1.0.0"
        }

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
