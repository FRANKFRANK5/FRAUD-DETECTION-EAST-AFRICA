# PROJECT OUTLINE

## Fraud Detection & Trust Scoring System
**Participant:** Frank Karani | **Challenge:** #04 | **Country:** Tanzania

---

## 1. PROJECT OVERVIEW

| Item | Description |
|------|-------------|
| **Project Name** | Fraud Detection & Trust Scoring System |
| **Challenge** | #04 - Fraud Detection & Trust Scoring |
| **Region** | East Africa (Tanzania, Kenya, Uganda) |
| **Participant** | Frank Karani |
| **Technology** | FastAPI, Python, SQLite, HTML/CSS/JS |

---

## 2. PROBLEM STATEMENT

Rental fraud is increasing across East Africa:
- Scammers post fake listings (phantom properties)
- Victims pay deposits for non-existent rentals
- No centralized trust scoring system exists
- Cross-border fraud between TZ, KE, UG is common

---

## 3. SOLUTION

A multi-factor fraud detection system that analyzes:

| Factor | Weight | Description |
|--------|--------|-------------|
| Price Anomaly | 35% | Compares against East African market data |
| User Behavior | 25% | Account age, verification status |
| Content Analysis | 20% | Keywords, images, description quality |
| Geographic | 10% | City and location validation |
| Metadata | 10% | Listing ID, price patterns |

---

## 4. DELIVERABLES

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | Fraud detection model | ✅ COMPLETE |
| 2 | Risk scoring system (0-100) | ✅ COMPLETE |
| 3 | 6 detection scenarios | ✅ COMPLETE |

---

## 5. DETECTION SCENARIOS (6)

| # | Scenario | Indicators |
|---|----------|------------|
| 1 | Phantom Listing | Price 60% below market, no images, new user |
| 2 | Price Anomaly | 40%+ below / 100%+ above market |
| 3 | Rapid Listing | 5+ listings/day, similar descriptions |
| 4 | Identity Theft | Unverified user, suspicious patterns |
| 5 | Payment Fraud | Western Union, overseas landlord |
| 6 | Image Fraud | Stock photos, low quality images |

---

## 6. EAST AFRICAN MARKET DATA

### Supported Countries
- Tanzania (TZ)
- Kenya (KE)
- Uganda (UG)

### Supported Cities (15 cities)

| Country | Cities |
|---------|--------|
| Tanzania | Dar es Salaam, Arusha, Mwanza, Zanzibar, Dodoma |
| Kenya | Nairobi, Mombasa, Kisumu, Nakuru, Eldoret |
| Uganda | Kampala, Entebbe, Jinja, Gulu, Mbarara |

### Price Reference (USD/month)

| City | 1BR | 2BR | 3BR | 4BR |
|------|-----|-----|-----|-----|
| Dar es Salaam | 350 | 550 | 800 | 1200 |
| Nairobi | 400 | 650 | 950 | 1400 |
| Kampala | 300 | 500 | 750 | 1100 |

---

## 7. TECHNOLOGY STACK

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Containerization | Docker |
| Testing | Pytest |
| Version Control | Git |

---

## 8. API ENDPOINTS

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/v1/detect` | Detect fraud in listing |
| GET | `/api/v1/trust-score/{user_id}` | Get user trust score |
| GET | `/api/v1/scenarios` | List detection scenarios |
| GET | `/api/docs` | Swagger documentation |

---

## 9. PROJECT STRUCTURE

rental-fraud-detection-eastafrica/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── config.py
│ ├── api/
│ │ ├── init.py
│ │ └── schemas.py
│ ├── trust_scoring/
│ │ ├── init.py
│ │ ├── calculator.py
│ │ ├── rules.py
│ │ └── weights.py
│ ├── models/
│ │ ├── init.py
│ │ ├── predict.py
│ │ └── train.py
│ ├── data/
│ │ ├── init.py
│ │ ├── features.py
│ │ ├── preprocess.py
│ │ └── sample_data.csv
│ ├── database/
│ │ ├── init.py
│ │ ├── db.py
│ │ └── queries.py
│ └── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
├── deployment/
│ ├── Dockerfile
│ └── docker-compose.yml
├── docs/
│ ├── architecture.md
│ ├── how_it_works.md
│ └── demo_instructions.md
├── notebooks/
│ └── exploration.ipynb
├── tests/
│ ├── test_api.py
│ ├── test_model.py
│ └── test_trust_scoring.py
├── requirements.txt
├── README.md
├── .gitignore
├── OUTLINE
└── TIMELINE
text


---

## 10. SECURITY FEATURES (OWASP Top 10)

| OWASP | Implementation |
|-------|----------------|
| A01:2021 | Rate limiting, CORS |
| A02:2021 | Secure headers (HSTS) |
| A03:2021 | Input validation (Pydantic) |
| A04:2021 | Security headers |
| A05:2021 | Trusted host middleware |
| A08:2021 | Input sanitization |
| A09:2021 | Request logging |

---

## 11. JUDGING CRITERIA

| Criteria | Weight | Status |
|----------|--------|--------|
| Security Depth | 30% | ✅ Implemented |
| Technical Implementation | 25% | ✅ Implemented |
| Business Relevance | 25% | ✅ Implemented |
| Innovation | 20% | ✅ Implemented |

---

## 12. SUBMISSION CHECKLIST

- [x] Fraud detection model
- [x] Risk scoring system (0-100)
- [x] 6 detection scenarios
- [x] East African market focus (TZ, KE, UG)
- [x] OWASP security compliance
- [x] API documentation (Swagger)
- [x] Frontend dashboard
- [x] README with setup instructions
- [x] Demo instructions for judges

---

**Last Updated:** May 2026 | **Frank Karani**
