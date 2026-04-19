from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_api_key(x_api_key: str = Header(None)):
    """
    Verifies the API key provided in the request headers.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing from headers (X-API-Key)"
        )
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    return x_api_key
