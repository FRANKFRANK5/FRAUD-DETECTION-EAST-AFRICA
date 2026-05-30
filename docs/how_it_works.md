# How It Works - User Guide

## Fraud Detection & Trust Scoring System
**Participant:** Frank Karani | **Challenge:** #04 | **Country:** Tanzania

---

## 1. What This System Does

This system detects **fraudulent rental listings** and calculates **trust scores** for users on East African property platforms (Tanzania, Kenya, Uganda).

---

## 2. Fraud Detection Process

### Step 1: Submit Listing Data

User submits listing information:
- Listing ID, Title, Price
- Location, City, Bedrooms
- Description, Images
- User ID, Account Age, Verification Status

### Step 2: System Analysis

The system analyzes **5 factors**:

| Factor | Weight | What It Checks |
|--------|--------|----------------|
| Price Anomaly | 35% | Compares price against market data for that city & bedrooms |
| User Behavior | 25% | Account age, verification status |
| Content Analysis | 20% | Keywords, images, description quality |
| Geographic | 10% | City and location validation |
| Metadata | 10% | Listing ID format, price patterns |

### Step 3: Results

The system returns:

| Field | Description |
|-------|-------------|
| `is_fraud` | TRUE/FALSE if fraudulent |
| `fraud_score` | 0-100 (higher = more likely fraud) |
| `risk_level` | LOW, MEDIUM, or HIGH |
| `reasons` | List of suspicious indicators |
| `trust_score` | 0-100 (higher = more trustworthy) |

---

## 3. Risk Level Interpretation

| Risk Level | Fraud Score | Trust Score | Action |
|------------|-------------|-------------|--------|
| **LOW** | 0-29% | 71-100 | ✅ Approve listing |
| **MEDIUM** | 30-59% | 41-70 | 🔍 Review manually |
| **HIGH** | 60-100% | 0-40 | 🚫 Reject / Flag |

---

## 4. Detection Scenarios (6 Total)

### Scenario 1: Phantom Listing
**Description:** Property doesn't physically exist

**Indicators:**
- Price 60% below market average
- No images provided
- New user account (<7 days)
- Urgent payment request

### Scenario 2: Price Anomaly
**Description:** Price significantly deviates from market

**Indicators:**
- 40%+ below market average
- 100%+ above market average
- No comparable listings in area

### Scenario 3: Rapid Listing
**Description:** User posts many listings quickly

**Indicators:**
- 5+ listings per day
- Similar descriptions
- Random locations across cities

### Scenario 4: Identity Theft
**Description:** Stolen or fake identity

**Indicators:**
- Unverified ID document
- Suspicious phone number
- Multiple accounts same device

### Scenario 5: Payment Fraud
**Description:** Deposit and payment scams

**Indicators:**
- Western Union request
- Overseas landlord
- No viewing allowed
- Refundable deposit pressure

### Scenario 6: Image Fraud
**Description:** Stock or stolen property photos

**Indicators:**
- Reverse image search match
- Inconsistent property features
- Low image quality

---

## 5. East African Market Data

### Supported Cities

| Country | Cities |
|---------|--------|
| Tanzania | Dar es Salaam, Arusha, Mwanza, Zanzibar, Dodoma |
| Kenya | Nairobi, Mombasa, Kisumu, Nakuru, Eldoret |
| Uganda | Kampala, Entebbe, Jinja, Gulu, Mbarara |

### Price Reference (Monthly Rent in USD)

| City | 1BR | 2BR | 3BR | 4BR |
|------|-----|-----|-----|-----|
| Dar es Salaam | $350 | $550 | $800 | $1,200 |
| Nairobi | $400 | $650 | $950 | $1,400 |
| Kampala | $300 | $500 | $750 | $1,100 |
| Arusha | $250 | $400 | $600 | $900 |
| Mombasa | $300 | $500 | $700 | $1,000 |
| Zanzibar | $400 | $650 | $1,000 | $1,500 |

---

## 6. Suspicious Keywords

The system flags listings containing these keywords:

| English | Swahili |
|---------|---------|
| urgent | haraka |
| deposit | amana |
| western union | tuma pesa |
| moneygram | nje ya nchi |
| overseas | wakala |
| agent fee | pesa ya mbele |
| no viewing | - |
| refundable | - |

---

## 7. Trust Score Calculation

Trust score is calculated based on:

| Factor | Impact |
|--------|--------|
| Account age | Older = higher trust |
| Verification status | Verified = +points |
| Historical listings | More listings = higher trust |
| Fraud reports | Reports = lower trust |

**Trust Score Range:**
- 70-100: APPROVE (High trust)
- 50-69: REVIEW (Medium trust)
- 0-49: REJECT (Low trust)

---

## 8. API Usage Examples

### Check Listing (cURL)

```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": "LST001",
    "title": "Modern Apartment",
    "price": 550,
    "location": "Masaki, Dar es Salaam",
    "city": "Dar es Salaam",
    "bedrooms": 2,
    "description": "Beautiful apartment with sea view",
    "has_images": true,
    "user_id": "USER001",
    "user_account_days": 365,
    "user_verified": true
  }'

Get Trust Score
bash

curl http://localhost:8000/api/v1/trust-score/USER001

Get Detection Scenarios
bash

curl http://localhost:8000/api/v1/scenarios

9. Running the System
Local Development
bash

# Install dependencies
pip install -r requirements.txt

# Run the API
python app/main.py

# Open browser
http://localhost:8000

Docker
bash

# Build
docker build -f deployment/Dockerfile -t fraud-detection .

# Run
docker run -p 8000:8000 fraud-detection

10. Testing Examples
Legitimate Listing (Low Risk)
Field	Value
Price	$550
City	Dar es Salaam
Bedrooms	2
Account Age	365 days
Verified	Yes
Has Images	Yes

Expected Result: LOW risk, Fraud Score < 30%
Fraudulent Listing (High Risk)
Field	Value
Price	$150
City	Dar es Salaam
Bedrooms	3
Account Age	1 day
Verified	No
Has Images	No
Description	"URGENT! Send deposit via Western Union"

Expected Result: HIGH risk, Fraud Score > 60%

Document Version: 1.0 | Last Updated: May 2026 | Frank Karani
text


---
