import json
from google import genai
from google.genai import types
from fastapi import HTTPException, status

from app.config import settings
from app.models import GeminiAnalysisResult, ScanType

# Initialize Client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
You are an expert Cybersecurity Threat Analyst for 'AI Cyber Shield'.
Your task is to analyze SMS messages, Emails, or URLs for phishing, scams, social engineering, malicious links, and fraud.

Guidelines:
1. Status must strictly be "Safe" or "Scam".
2. Risk Score must be between 0 (safe) and 100 (high danger).
3. Risk Level must be "Low" (0-30), "Medium" (31-70), or "High" (71-100).
4. Provide a clear reason highlighting specific red flags (e.g., suspicious domain, urgent tone, request for credentials).
5. Provide a direct recommendation for what the user should do next.
"""

async def analyze_content_with_gemini(scan_type: ScanType, content: str) -> GeminiAnalysisResult:
    prompt = f"Analyze the following {scan_type.value.upper()} content for potential scam or cyber security threats:\n\n\"{content}\""

    try:
        # Async call using client.aio
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=GeminiAnalysisResult,
                temperature=0.1,
            ),
        )
        
        result_dict = json.loads(response.text)
        return GeminiAnalysisResult(**result_dict)

    except Exception as e:
        print(f"Gemini Async Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini AI processing failed: {str(e)}"
        )