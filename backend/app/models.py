from enum import Enum
from pydantic import BaseModel, Field

class ScanType(str, Enum):
    SMS = "sms"
    EMAIL = "email"
    URL = "url"

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusType(str, Enum):
    SAFE = "Safe"
    SCAM = "Scam"

# --- API Request ---
class ScanRequest(BaseModel):
    scan_type: ScanType = Field(..., description="Type of input: sms, email, or url")
    content: str = Field(..., min_length=1, max_length=10000, description="Content to evaluate")

# --- Structured Output Schema for Gemini ---
class GeminiAnalysisResult(BaseModel):
    status: StatusType
    risk_score: int = Field(..., ge=0, le=100, description="Risk score from 0 (safe) to 100 (scam)")
    risk_level: RiskLevel
    reason: str = Field(..., description="Detailed explanation of why it is flagged or safe")
    recommendation: str = Field(..., description="Actionable advice for the user")

# --- API Response ---
class ScanResponse(BaseModel):
    scan_id: str
    scan_type: ScanType
    content: str
    status: StatusType
    risk_score: int
    risk_level: RiskLevel
    reason: str
    recommendation: str
    created_at: str