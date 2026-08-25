from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Hackathon Bypass Mode:
    Token check ko bypass karke dummy user return kar rahe hain
    taaki demo smoothly chale bina login ke!
    """
    return {
        "uid": "hackathon_demo_user_123",
        "email": "demo_user@cybershield.com",
    }