# Demo Instructions for Judges

## Fraud Detection & Trust Scoring System
**Participant:** Frank Karani | **Challenge:** #04 | **Country:** Tanzania

---

## Quick Demo (5 Minutes)

### Step 1: Start the Application

```bash
# Open terminal in project folder
cd rental-fraud-detection-eastafrica

# Install dependencies
pip install -r requirements.txt

# Run the API
python app/main.py

Expected output:
text

INFO: Uvicorn running on http://0.0.0.0:8000

Step 2: Open Web Dashboard

Open browser and navigate to:
text

http://localhost:8000

You will see:

    🛡️ Fraud Detection & Trust Scoring header

    Check Rental Listing form (left side)

    Trust Score Check (right side)

    Detection Scenarios list

Test Case 1: Legitimate Listing (Low Risk)
Using Web Dashboard:

    Fill the form with:

        Listing ID: LST-LEGIT-001

        Title: Modern 2BR Apartment with Ocean View

        Price: 550

        City: Dar es Salaam

        Bedrooms: 2

        Location: Masaki, Dar es Salaam, Tanzania

        Description: Beautiful modern apartment with sea view, secure area with 24/7 security

        Has Images: Yes

        User ID: VERIFIED_USER

        Account Age: 365

        Verified User: Yes

    Click "🚨 Detect Fraud"

Expected Result:
text

✅ No Fraud Detected
Fraud Score: 0-25%
Risk Level: LOW
Trust Score: 75-100%
Reasons: (none or minimal)

Using API (cURL):
bash

curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": "LST001",
    "title": "Modern 2BR Apartment",
    "price": 550,
    "location": "Masaki, Dar es Salaam",
    "city": "Dar es Salaam",
    "bedrooms": 2,
    "description": "Beautiful apartment with sea view, secure area",
    "has_images": true,
    "user_id": "VERIFIED_USER",
    "user_account_days": 365,
    "user_verified": true
  }'

Test Case 2: Fraudulent Listing (High Risk)
Using Web Dashboard:

    Fill the form with:

        Listing ID: SCAM-001

        Title: AMAZING DEAL!!! 3BR HOUSE

        Price: 150

        City: Dar es Salaam

        Bedrooms: 3

        Location: Somewhere

        Description: URGENT! Send deposit via Western Union to secure this amazing property! Owner is overseas. First come first serve!

        Has Images: No

        User ID: NEW_USER

        Account Age: 1

        Verified User: No

    Click "🚨 Detect Fraud"

Expected Result:
text

🚨 FRAUD DETECTED!
Fraud Score: 60-100%
Risk Level: HIGH
Trust Score: 0-40%
Reasons:
- ⚠️ Price is 60% below market - Classic phantom listing
- ⚠️ New account (less than 7 days)
- ⚠️ Suspicious keyword: 'urgent'
- ⚠️ No images provided
- ⚠️ Unverified user

Using API (cURL):
bash

curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": "SCAM001",
    "title": "AMAZING DEAL!!!",
    "price": 150,
    "location": "Somewhere",
    "city": "Dar es Salaam",
    "bedrooms": 3,
    "description": "URGENT! Send deposit via Western Union!",
    "has_images": false,
    "user_id": "NEW_USER",
    "user_account_days": 1,
    "user_verified": false
  }'

Test Case 3: Trust Score Check
Using Web Dashboard:

    Go to right side card "⭐ Trust Score Check"

    Enter User ID: USER001

    Click "📊 Calculate Trust Score"

Expected Result:
text

Trust Score: 50-94%
Risk Level: LOW/MEDIUM/HIGH
Recommendation: APPROVE/REVIEW/REJECT

Using API (cURL):
bash

curl http://localhost:8000/api/v1/trust-score/USER001

Test Case 4: View Detection Scenarios
Using Web Dashboard:

Scroll down to "⚠️ Detection Scenarios" section on the right side.
Expected Result:

List of 6 scenarios:

    Phantom Listing

    Price Anomaly

    Rapid Listing

    Identity Theft

    Payment Fraud

    Image Fraud

Using API (cURL):
bash

curl http://localhost:8000/api/v1/scenarios

Test Case 5: API Documentation

Open browser:
text

http://localhost:8000/api/docs

You will see Swagger UI with all endpoints:

    POST /api/v1/detect - Try it out

    GET /api/v1/trust-score/{user_id} - Try it out

    GET /api/v1/scenarios - Try it out

Quick Comparison Table
Test Case	Price	Account Age	Verified	Images	Expected Risk
Legitimate	$550	365 days	Yes	Yes	LOW
Fraudulent	$150	1 day	No	No	HIGH
Suspicious	$300	5 days	No	Yes	MEDIUM
Troubleshooting
Issue: API won't start
bash

# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process or change port in app/config.py

Issue: Frontend shows no data
bash

# Make sure API is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}

Issue: Module not found
bash

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

Demo Video Script (3 Minutes)

0:00-0:30 - Introduction

    "Hello judges, my name is Frank Karani from Tanzania. This is my Fraud Detection & Trust Scoring System for the East African rental market."

0:30-1:00 - Show legitimate listing test

    "First, I'll test a legitimate listing from Dar es Salaam. Price $550, verified user, has images. As expected, the system returns LOW risk."

1:00-1:30 - Show fraudulent listing test

    "Now I'll test a fraudulent listing. Price $150, new user, no images, urgent deposit request. The system correctly detects HIGH risk with clear reasons."

1:30-2:00 - Show trust score and scenarios

    "Here's the trust score check for a user, and the 6 detection scenarios the system uses."

2:00-2:30 - Show API documentation

    "Finally, the complete API documentation is available at /api/docs with Swagger UI."

2:30-3:00 - Conclusion

    "Thank you for judging. The system is fully functional and ready for deployment."

Submission Checklist

    System runs without errors

    API endpoints work

    Web dashboard displays correctly

    Legitimate listing shows LOW risk

    Fraudulent listing shows HIGH risk

    Trust score calculates correctly

    6 detection scenarios listed

    East African cities supported (TZ, KE, UG)

Good luck with the judging! - Frank Karani

Document Version: 1.0 | Last Updated: May 2026
text


---
Submission Checklist

    System runs without errors

    API endpoints work

    Web dashboard displays correctly

    Legitimate listing shows LOW risk

    Fraudulent listing shows HIGH risk

    Trust score calculates correctly

    6 detection scenarios listed

    East African cities supported (TZ, KE, UG)