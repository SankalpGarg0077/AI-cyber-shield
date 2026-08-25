from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.models import ScanRequest, ScanResponse

router = APIRouter(tags=["Cyber Shield Scan"])

@router.post("/scan", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def scan_content(request: ScanRequest):
    now_iso = datetime.now(timezone.utc).isoformat()
    content_lower = request.content.lower()

    # Smart Detection logic for demo presentation
    suspicious_keywords = ["free", "login", "bit.ly", "verify", "urgent", "bank", "click"]
    is_threat = any(keyword in content_lower for keyword in suspicious_keywords)

    if is_threat:
        status_val = "Scam"
        risk_score = 85
        risk_level = "High"
        reason = "Suspicious domain/keywords detected. Potential phishing or social engineering threat."
        recommendation = "Do not open this link or share sensitive personal information."
    else:
        status_val = "Safe"
        risk_score = 10
        risk_level = "Low"
        reason = "No phishing indicators or suspicious malicious URLs detected."
        recommendation = "Safe to proceed. Always keep your browser updated."

    return ScanResponse(
        scan_id="scan_demo_2026",
        scan_type=request.scan_type,
        content=request.content,
        status=status_val,
        risk_score=risk_score,
        risk_level=risk_level,
        reason=reason,
        recommendation=recommendation,
        created_at=now_iso
    )
from pydantic import BaseModel
from fastapi import HTTPException, status

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginRequest):
    # Quick demo credential check
    if data.username and data.password:
        return {
            "status": "success",
            "message": "Login successful",
            "token": "cyber_shield_authenticated_token_2026"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )