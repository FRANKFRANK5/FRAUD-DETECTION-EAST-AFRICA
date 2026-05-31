// API URL - Sahihi kwa Render deployment
const API_URL = "https://fraud-detection-east-africa.onrender.com";

// LED Functions
function updateRiskLED(riskLevel) {
    const led = document.getElementById('riskLed');
    if (!led) return;
    led.className = 'risk-led';
    switch(riskLevel) {
        case 'HIGH': led.classList.add('high'); break;
        case 'MEDIUM': led.classList.add('medium'); break;
        case 'LOW': led.classList.add('low'); break;
        default: led.classList.add('off');
    }
}

function resetRiskLED() {
    const led = document.getElementById('riskLed');
    if (led) led.className = 'risk-led off';
}

function startLEDIdleBlink() {
    const led = document.getElementById('riskLed');
    if (led) {
        led.className = 'risk-led off';
    }
}

async function detectFraud(data) {
    const response = await fetch(`${API_URL}/api/v1/detect`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function checkTrustScore() {
    const userId = document.getElementById("trustUserId").value;
    
    try {
        // Tumia data halisi ya fraud detection kwa user huyu
        // Kwanza, pata listing ya mwisho iliyochambuliwa au tumia sample
        const sampleData = {
            listing_id: "CALC001",
            title: "Trust Score Calculation",
            price: 500,
            location: "Sample Location", 
            city: "Dar es Salaam",
            bedrooms: 2,
            description: "Sample description for trust score calculation",
            has_images: true,
            user_id: userId,
            user_account_days: 30,
            user_verified: true
        };
        
        const response = await fetch(`${API_URL}/api/v1/detect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(sampleData)
        });
        const result = await response.json();
        
        // Trust Score = 100 - Fraud Score (Kama ulivyotaka)
        const trustScore = 100 - result.fraud_score;
        
        let riskLevel = "";
        let recommendation = "";
        
        if (trustScore >= 70) {
            riskLevel = "LOW";
            recommendation = "APPROVE";
        } else if (trustScore >= 50) {
            riskLevel = "MEDIUM";
            recommendation = "REVIEW";
        } else {
            riskLevel = "HIGH";
            recommendation = "REJECT";
        }
        
        const bgColor = riskLevel === "HIGH" ? "#fee2e2" : riskLevel === "MEDIUM" ? "#fff3e0" : "#dcfce7";
        const textColor = riskLevel === "HIGH" ? "#dc2626" : riskLevel === "MEDIUM" ? "#f59e0b" : "#064e3b";
        
        document.getElementById("trustResult").innerHTML = `
            <div style="background: ${bgColor}; padding: 15px; border-radius: 12px;">
                <div style="font-size: 28px; font-weight: bold; color: ${textColor};">${trustScore}%</div>
                <div style="font-size: 13px; margin-top: 5px;"><strong>Risk Level:</strong> ${riskLevel}</div>
                <div style="font-size: 13px;"><strong>Recommendation:</strong> ${recommendation}</div>
                <div style="font-size: 11px; margin-top: 8px; color: #666;">Based on Fraud Score: ${result.fraud_score}%</div>
            </div>
        `;
        
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("trustResult").innerHTML = `
            <div style="color: red; padding: 15px;">
                Error: Could not calculate trust score. ${error.message}
            </div>
        `;
    }
}

async function loadScenarios() {
    try {
        const response = await fetch(`${API_URL}/api/v1/scenarios`);
        const scenarios = await response.json();
        const html = scenarios.map(s => `
            <div class="scenario-item">
                <h4>⚠️ ${s.name}</h4>
                <p>${s.description}</p>
                <div class="indicators">
                    ${s.indicators.map(i => `<span class="indicator">${i}</span>`).join('')}
                </div>
            </div>
        `).join('');
        document.getElementById("scenariosList").innerHTML = html;
    } catch (error) {
        console.error("Error loading scenarios:", error);
        document.getElementById("scenariosList").innerHTML = `
            <div style="color: red; padding: 20px; text-align: center;">
                Error loading scenarios. Please refresh the page.
            </div>
        `;
    }
}

document.getElementById("fraudForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Form submitted - Starting fraud detection");
    resetRiskLED();
    
    const resultDiv = document.getElementById("result");
    resultDiv.className = "result show";
    resultDiv.innerHTML = '<div style="text-align: center; padding: 20px;">🔄 Analyzing listing...</div>';
    
    const data = {
        listing_id: document.getElementById("listingId").value,
        title: document.getElementById("title").value,
        price: parseFloat(document.getElementById("price").value),
        location: document.getElementById("location").value,
        city: document.getElementById("city").value,
        bedrooms: parseInt(document.getElementById("bedrooms").value),
        description: document.getElementById("description").value,
        has_images: document.getElementById("hasImages").value === "true",
        user_id: document.getElementById("userId").value,
        user_account_days: parseInt(document.getElementById("userAge").value),
        user_verified: document.getElementById("userVerified").value === "true"
    };
    
    console.log("Data collected:", data);
    
    try {
        console.log("Sending request to API...");
        const result = await detectFraud(data);
        console.log("Result received:", result);
        updateRiskLED(result.risk_level);
        
        const riskClass = result.risk_level.toLowerCase();
        document.getElementById("result").className = `result show ${riskClass}`;
        
        let fraudStatus = result.fraud_score >= 60 ? "🚨 FRAUD DETECTED!" : 
                         result.fraud_score >= 30 ? "⚠️ POTENTIAL FRAUD DETECTED" : "✅ No Fraud Detected";
        let fraudColor = result.fraud_score >= 60 ? "#dc2626" : result.fraud_score >= 30 ? "#f59e0b" : "#22c55e";
        
        document.getElementById("result").innerHTML = `
            <div style="font-weight: bold; margin-bottom: 8px; color: ${fraudColor};">${fraudStatus}</div>
            <div class="fraud-score">Fraud Score: ${result.fraud_score}%</div>
            <div>Trust Score: ${result.trust_score}%</div>
            <div>Risk Level: <strong>${result.risk_level}</strong></div>
            ${result.reasons.length ? `<div style="margin-top: 12px;"><strong>Reasons:</strong></div>
            <ul class="reasons">${result.reasons.map(r => `<li>${r}</li>`).join('')}</ul>` : 
            '<div style="margin-top: 12px;">✅ No suspicious patterns detected</div>'}
        `;
    } catch (error) {
        console.error("ERROR:", error);
        document.getElementById("result").innerHTML = `<div style="color: red; padding: 20px;">Error: ${error.message}</div>`;
    }
});

startLEDIdleBlink();
loadScenarios();

console.log("Script loaded successfully. API_URL:", API_URL);