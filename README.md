# 🛡️ Fraud Detection & Trust Scoring System
## East African Rental Market Intelligence Platform

**Participant:** Frank Karani
**Country:** Tanzania
**Challenge:** #04 - Fraud Detection & Trust Scoring
**Institution:** IAA (Institute of Accountancy Arusha) - Year One
**Student:** This project developed by **First year student 2025/2026**
---

## 📌 Overview

This system detects fraudulent rental listings in the East African market (Tanzania, Kenya, Uganda) using a multi-factor risk analysis engine.

It is designed to help users identify suspicious listings before making financial commitments, improving trust and safety in digital property marketplaces.

**Live Demo:** https://fraud-detection-east-africa.onrender.com
**GitHub:** https://github.com/FRANKFRANK5/FRAUD-DETECTION-EAST-AFRICA

## 📸 Live Demo Screenshots

### 1. Safe Listing - Trust Score 100%
![Safe Listing](Screenshot_20260602-163955.jpg)

### 2. Fraud Detected - 73% Risk
![Fraud Detected](Screenshot_20260602-164031.jpg)

### 3. Input Form
![Input Form](Screenshot_20260602-163816.jpg)

---

## ⚙️ How It Works

The system evaluates each listing using five weighted intelligence factors:

### 1. 💰 Price Anomaly Detection (35%)
Compares listing price against East African market averages to identify unrealistic or suspicious pricing patterns.

### 2. 👤 User Behavior Analysis (25%)
Evaluates account age, verification status, and behavioral patterns to detect potentially fraudulent users.

### 3. 📝 Content Intelligence (20%)
Analyzes listing descriptions for suspicious keywords, missing details, and image presence or reuse.

### 4. 📍 Geographic Validation (10%)
Verifies that listed locations are consistent with valid and expected East African rental regions.

### 5. 🧾 Metadata Analysis (10%)
Examines listing structure, identifiers, and pricing patterns associated with fraudulent activity.

---

## 📊 System Output

For each listing, the system generates:

| Output | Description |
|--------|-------------|
| **Fraud Score** | 0–100% (higher = more likely fraudulent) |
| **Trust Score** | 0–100% (higher = more trustworthy) |
| **Risk Level** | LOW / MEDIUM / HIGH |
| **Recommendation** | APPROVE / REVIEW / REJECT |
| **Reasons** | Explanation of detected risk factors |

**Formula:** Trust Score = 100 - Fraud Score

---

## 🚨 Detection Scenarios (6 Core Fraud Types)

| # | Scenario | Description |
|---|----------|-------------|
| 1 | **Phantom Listing** | Property does not physically exist |
| 2 | **Price Anomaly** | Significant deviation from market price |
| 3 | **Rapid Listing Abuse** | Excessive posting in short time |
| 4 | **Identity Theft** | Fake or stolen user identity |
| 5 | **Payment Fraud** | Advance payment and deposit scams |
| 6 | **Image Fraud** | Stock or reused property images |

---

## 🔄 Methodology Transfer

This system is inspired by anomaly detection techniques from the **Kaggle Credit Card Fraud Detection dataset** (285,000+ transactions).

| Kaggle Feature | Rental Fraud Equivalent | Weight |
|----------------|------------------------|--------|
| Amount | Price anomalies | 35% |
| Time | User account age & activity | 25% |
| V1–V28 (PCA features) | Content intelligence signals | 20% |
| Transaction patterns | Geographic & metadata validation | 20% |

---

## 🛠️ Technical Implementation

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI with Pydantic validation |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Server** | Uvicorn |
| **Database** | SQLite |
| **Deployment** | Render (Live Cloud Hosting) |
| **Architecture** | REST API-based scoring engine |
| **Security** | Input validation, rate limiting, OWASP compliance |

---

## 🌍 East African Market Coverage

The system is optimized for the East African rental ecosystem:

| Country | Cities |
|---------|--------|
| 🇹🇿 **Tanzania** | Dar es Salaam, Arusha, Mwanza, Zanzibar, Dodoma |
| 🇰🇪 **Kenya** | Nairobi, Mombasa, Kisumu, Nakuru, Eldoret |
| 🇺🇬 **Uganda** | Kampala, Entebbe, Jinja, Gulu, Mbarara |

**Market Price References (USD/month):**

| City | 1BR | 2BR | 3BR | 4BR |
|------|-----|-----|-----|-----|
| Dar es Salaam | $350 | $550 | $800 | $1,200 |
| Nairobi | $400 | $650 | $950 | $1,400 |
| Kampala | $300 | $500 | $750 | $1,100 |

---

## 🧪 Test Examples

### ✅ Legitimate Listing (LOW RISK)

| Field | Value |
|-------|-------|
| Price | $550 for 2BR in Dar es Salaam |
| Account Age | 365 days |
| Verified | Yes |
| Has Images | Yes |

**Result:**
- Fraud Score: 0%
- Trust Score: 100%
- Risk Level: LOW
- Recommendation: APPROVE

---

### 🚨 Fraudulent Listing (HIGH RISK)

| Field | Value |
|-------|-------|
| Price | $150 for 3BR in Dar es Salaam (60% below market) |
| Account Age | 1 day |
| Verified | No |
| Has Images | No |
| Description | "URGENT! Send deposit via Western Union" |

**Result:**
- Fraud Score: 73%
- Trust Score: 27%
- Risk Level: HIGH
- Recommendation: REJECT

---

## 🎯 Impact

This system helps:

- ✅ Prevent rental fraud before payments occur
- ✅ Improve trust between tenants and landlords
- ✅ Strengthen digital property platforms
- ✅ Support safer financial decisions
- ✅ Enhance transparency in East African rental markets

---

## 🛡️ Cold-Start Prevention Strategy

The system applies rule-based risk inflation for new or suspicious accounts:

| Condition | Fraud Score Increase |
|-----------|---------------------|
| New accounts (<7 days) | +18 points |
| Unverified users | +15 points |
| No images | +12 points |

👉 This prevents scammers from exploiting system trust gaps.

---

## 🔮 Future Integration

Designed for integration with East African digital identity systems:

| Country | System | Purpose |
|---------|--------|---------|
| Tanzania | NIDA e-KYC | User identity verification |
| Tanzania | NaPA Digital Addressing | Location validation |
| Kenya | Huduma Namba | National ID verification |
| Uganda | NIN | Identity authentication |

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run API
python app/main.py

# Open in browser
http://localhost:8000
http://localhost:8000/docs

📡 API Endpoints
Method	Endpoint	Description
POST	/api/v1/detect	Detect fraud in rental listing
GET	/api/v1/trust-score/{user_id}	Get user trust score (0–100)
GET	/api/v1/scenarios	List all 6 detection scenarios
📁 Project Structure
text

rental-fraud-detection-eastafrica/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/schemas.py
│   ├── trust_scoring/ (calculator, rules, weights)
│   ├── models/ (predict, train)
│   ├── data/ (features, preprocess, sample_data.csv)
│   ├── database/ (db, queries)
│   └── frontend/ (index.html, style.css, script.js)
├── deployment/ (Dockerfile, docker-compose.yml)
├── docs/ (architecture.md, how_it_works.md, demo_instructions.md)
├── notebooks/ (exploration.ipynb)
├── tests/ (test_api.py, test_model.py, test_trust_scoring.py)
├── requirements.txt
├── README.md
├── OUTLINE
└── TIMELINE

🏁 Conclusion

This is a real-time fraud detection and trust scoring system that applies data-driven risk analysis to rental listings, helping build safer and more reliable digital property ecosystems across East Africa.
📞 ##Contact

###Frank Karani

    Email: frankkarani146@gmail.com

    Institution: IAA (Institute of Accountancy Arusha)
    First year student 2025/2026

    Country: Tanzania

    Challenge: #04 - Fraud Detection & Trust Scoring

"Technology should not only connect people — it should protect them."

— Frank Karani
First year student
