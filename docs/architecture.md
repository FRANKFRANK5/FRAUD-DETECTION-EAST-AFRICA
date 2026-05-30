# System Architecture Document

## Fraud Detection & Trust Scoring System
**Participant:** Frank Karani | **Challenge:** #04 | **Country:** Tanzania

---

## 1. Overview

This document describes the architecture of the Fraud Detection & Trust Scoring System for the East African rental market (Tanzania, Kenya, Uganda).

---

## 2. High-Level Architecture

┌─────────────────────────────────────────────────────────────────┐
│ Client Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │ Web UI │ │ REST API │ │ Swagger Documentation │ │
│ │ (HTML/CSS) │ │ (Browser) │ │ (/api/docs) │ │
│ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ API Gateway Layer │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ FastAPI Application ││
│ │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────┐ ││
│ │ │ CORS │ │ Rate │ │ Trusted │ │ Input │ ││
│ │ │ Middleware│ │ Limiter │ │ Host │ │Validation│ ││
│ │ └───────────┘ └───────────┘ └───────────┘ └─────────┘ ││
│ └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ Business Logic Layer │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Fraud Detection Engine ││
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ ││
│ │ │ Price │ │ User │ │ Content │ ││
│ │ │ Anomaly │ │ Behavior │ │ Analysis │ ││
│ │ │ (35%) │ │ (25%) │ │ (20%) │ ││
│ │ └─────────────┘ └─────────────┘ └─────────────────────┘ ││
│ │ ┌─────────────┐ ┌─────────────┐ ││
│ │ │ Geographic │ │ Metadata │ ││
│ │ │ Validation │ │ Analysis │ ││
│ │ │ (10%) │ │ (10%) │ ││
│ │ └─────────────┘ └─────────────┘ ││
│ └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ Data Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │ SQLite │ │ CSV Data │ │ ML Model (Optional) │ │
│ │ Database │ │ (Market) │ │ (.pkl file) │ │
│ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘


---

## 3. Component Details

### 3.1 API Layer (FastAPI)

| Component | Description |
|-----------|-------------|
| **Main Application** | `app/main.py` - Entry point |
| **Routes** | `/api/v1/detect`, `/api/v1/trust-score`, `/api/v1/scenarios` |
| **Middleware** | CORS, Rate Limiting, Trusted Hosts |

### 3.2 Fraud Detection Engine

| Factor | Weight | Description |
|--------|--------|-------------|
| Price Anomaly | 35% | Compares against East African market data |
| User Behavior | 25% | Account age, verification status |
| Content Analysis | 20% | Keywords, images, description quality |
| Geographic | 10% | City and location validation |
| Metadata | 10% | Listing ID, price patterns |

### 3.3 Data Flow
User submits listing data via Web UI or API

Request validation (Pydantic schemas)

Rate limiting check

Feature extraction

Fraud detection calculation

Trust score calculation

Response returned to client

Optional: Save to database


---

## 4. Security Architecture (OWASP Compliance)

| OWASP Category | Implementation |
|----------------|----------------|
| A01:2021 - Broken Access Control | Rate limiting, CORS |
| A02:2021 - Cryptographic Failures | Secure headers (HSTS) |
| A03:2021 - Injection | Input validation (Pydantic) |
| A04:2021 - Insecure Design | Security headers |
| A05:2021 - Security Misconfiguration | Trusted host middleware |
| A06:2021 - Vulnerable Components | Regular updates |
| A07:2021 - Identification Failures | Session validation |
| A08:2021 - Software Integrity | Input sanitization |
| A09:2021 - Monitoring | Request logging |
| A10:2021 - SSRF | Host header validation |

---

## 5. Deployment Architecture
┌─────────────────────────────────────────────────────────────────┐
│ Docker Container │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Python 3.11-slim ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ Uvicorn (ASGI Server) │││
│ │ │ ┌─────────────────────────────────────────────────────┐│││
│ │ │ │ FastAPI Application ││││
│ │ │ └─────────────────────────────────────────────────────┘│││
│ │ └─────────────────────────────────────────────────────────┘││
│ └─────────────────────────────────────────────────────────────┘│
│ Port: 8000 │
└─────────────────────────────────────────────────────────────────┘


---

## 6. Technology Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Containerization | Docker |
| Testing | Pytest |

---

## 7. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/api/v1/detect` | Fraud detection |
| GET | `/api/v1/trust-score/{user_id}` | Trust score |
| GET | `/api/v1/scenarios` | Detection scenarios |
| GET | `/api/docs` | Swagger documentation |

---

## 8. East African Market Data

### Supported Cities

| Country | Cities |
|---------|--------|
| Tanzania | Dar es Salaam, Arusha, Mwanza, Zanzibar, Dodoma |
| Kenya | Nairobi, Mombasa, Kisumu, Nakuru, Eldoret |
| Uganda | Kampala, Entebbe, Jinja, Gulu, Mbarara |

### Price Ranges (USD/month)

| City | 1BR | 2BR | 3BR | 4BR |
|------|-----|-----|-----|-----|
| Dar es Salaam | $350 | $550 | $800 | $1,200 |
| Nairobi | $400 | $650 | $950 | $1,400 |
| Kampala | $300 | $500 | $750 | $1,100 |

---

## 9. Error Handling

All errors are handled gracefully with appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (validation error)
- `422` - Unprocessable Entity
- `429` - Too Many Requests (rate limit)
- `500` - Internal Server Error

---

*Document Version: 1.0 | Last Updated: May 2026 | Frank Karani*