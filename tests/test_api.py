"""
API tests for Fraud Detection System
Tests all API endpoints functionality
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


class TestAPI:
    """Test class for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Fraud Detection & Trust Scoring"
        assert data["participant"] == "Frank Karani"
        assert data["status"] == "operational"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_detect_fraud_legitimate(self):
        """Test fraud detection with legitimate listing"""
        test_data = {
            "listing_id": "TEST001",
            "title": "Modern 2BR Apartment",
            "price": 550.0,
            "location": "Masaki, Dar es Salaam",
            "city": "Dar es Salaam",
            "bedrooms": 2,
            "description": "Beautiful apartment with sea view, secure area",
            "has_images": True,
            "user_id": "VERIFIED_USER",
            "user_account_days": 365,
            "user_verified": True
        }
        
        response = client.post("/api/v1/detect", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "is_fraud" in data
        assert "fraud_score" in data
        assert "risk_level" in data
    
    def test_detect_fraud_fraudulent(self):
        """Test fraud detection with fraudulent listing"""
        test_data = {
            "listing_id": "SCAM001",
            "title": "AMAZING DEAL!!!",
            "price": 150.0,
            "location": "Somewhere",
            "city": "Dar es Salaam",
            "bedrooms": 3,
            "description": "URGENT! Send deposit via Western Union!",
            "has_images": False,
            "user_id": "NEW_USER",
            "user_account_days": 1,
            "user_verified": False
        }
        
        response = client.post("/api/v1/detect", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["fraud_score"] >= 30
    
    def test_trust_score_endpoint(self):
        """Test trust score endpoint"""
        user_id = "TEST_USER_123"
        response = client.get(f"/api/v1/trust-score/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert "trust_score" in data
        assert 0 <= data["trust_score"] <= 100
        assert data["recommendation"] in ["APPROVE", "REVIEW", "REJECT"]
    
    def test_scenarios_endpoint(self):
        """Test detection scenarios endpoint"""
        response = client.get("/api/v1/scenarios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 6
        for scenario in data:
            assert "name" in scenario
            assert "description" in scenario
            assert "indicators" in scenario
    
    def test_invalid_listing_data(self):
        """Test API handles invalid data gracefully"""
        test_data = {
            "listing_id": "",
            "title": "",
            "price": -100,
            "city": "Invalid City",
            "bedrooms": 20
        }
        
        response = client.post("/api/v1/detect", json=test_data)
        assert response.status_code in [200, 422]
    
    def test_missing_fields(self):
        """Test API handles missing fields"""
        test_data = {
            "listing_id": "TEST001",
            "title": "Test"
        }
        
        response = client.post("/api/v1/detect", json=test_data)
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])