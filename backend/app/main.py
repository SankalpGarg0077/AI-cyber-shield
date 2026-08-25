from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI(title="AI Cyber Shield")

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class ScanRequest(BaseModel):
    scan_type: str
    content: str

@app.post("/login")
async def login(data: LoginRequest):
    if data.username and data.password:
        return {"status": "success", "message": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.post("/scan", status_code=201)
async def scan_content(request: ScanRequest):
    now_iso = datetime.now(timezone.utc).isoformat()
    content_lower = request.content.lower()

    suspicious_keywords = ["free", "login", "bit.ly", "verify", "urgent", "bank", "click", "claim"]
    is_threat = any(keyword in content_lower for keyword in suspicious_keywords)

    if is_threat:
        return {
            "scan_id": "scan_101",
            "scan_type": request.scan_type,
            "content": request.content,
            "status": "Scam",
            "risk_score": 85,
            "risk_level": "High",
            "reason": "Suspicious phishing patterns or domain links detected.",
            "recommendation": "Do not enter credentials or click on this link.",
            "created_at": now_iso
        }
    else:
        return {
            "scan_id": "scan_102",
            "scan_type": request.scan_type,
            "content": request.content,
            "status": "Safe",
            "risk_score": 10,
            "risk_level": "Low",
            "reason": "No security threats or phishing indicators found.",
            "recommendation": "Safe to visit.",
            "created_at": now_iso
        }