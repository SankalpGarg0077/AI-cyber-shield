const API_BASE_URL = "http://127.0.0.1:8000";

// Auth Guard: Agar user bina login index.html khele toh login page par bhej do
if (!localStorage.getItem("user_authenticated")) {
    window.location.href = "login.html";
}

async function analyzeText() {
    const inputElement = document.getElementById("scanInput");
    const loader = document.getElementById("loader");
    const resultCard = document.getElementById("resultCard");
    const resultContent = document.getElementById("resultContent");

    if (!inputElement) return;

    let inputVal = inputElement.value.trim();
    inputVal = inputVal.replace(/^\[|\]$/g, '');

    if (!inputVal) {
        alert("Please enter a valid URL or text to scan!");
        return;
    }

    loader.classList.remove("hidden");
    resultCard.classList.add("hidden");

    const scanType = (inputVal.startsWith("http://") || inputVal.startsWith("https://")) ? "url" : "text";

    try {
        const response = await fetch(`${API_BASE_URL}/scan`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                scan_type: scanType,
                content: inputVal
            })
        });

        const data = await response.json();
        loader.classList.add("hidden");
        resultCard.classList.remove("hidden");

        if (response.ok) {
            const isSafe = data.status.toLowerCase() === "safe";
            const badgeColor = isSafe ? "#4ade80" : "#ef4444";
            
            resultContent.innerHTML = `
                <div style="text-align: left; background: #0f172a; padding: 18px; border-radius: 8px; border: 1px solid #334155;">
                    <p style="margin-bottom: 8px;"><strong>Status:</strong> <span style="color: ${badgeColor}; font-weight: bold;">${data.status}</span></p>
                    <p style="margin-bottom: 8px;"><strong>Risk Level:</strong> <span style="color: #facc15;">${data.risk_level}</span></p>
                    <p style="margin-bottom: 8px;"><strong>Risk Score:</strong> ${data.risk_score}/100</p>
                    <p style="margin-bottom: 8px;"><strong>Reason:</strong> ${data.reason}</p>
                    <p style="margin-bottom: 0;"><strong>Recommendation:</strong> ${data.recommendation}</p>
                </div>
            `;
        } else {
            resultContent.innerHTML = `<p style="color: #f87171;">Scan Error: ${JSON.stringify(data.detail)}</p>`;
        }

    } catch (error) {
        loader.classList.add("hidden");
        alert("Backend network error! Ensure FastAPI server is running.");
    }
}

function logout() {
    localStorage.removeItem("user_authenticated");
    window.location.href = "login.html";
}