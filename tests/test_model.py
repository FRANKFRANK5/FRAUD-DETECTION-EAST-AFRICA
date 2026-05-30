"""
Model tests for Fraud Detection System
Tests fraud detection model functionality
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.trust_scoring.calculator import FraudDetector
from app.api.schemas import ListingRequest


class TestFraudDetector:
    """Test class for fraud detection model"""
    
    def setup_method(self):
        """Setup before each test"""
        self.detector = FraudDetector()
    
    def test_price_anomaly_detection(self):
        """Test price anomaly detection"""
        # Test too cheap listing
        cheap_listing = ListingRequest(
            listing_id="TEST001",
            title="Cheap House",
            price=150.0,
            location="Dar es Salaam",
            city="Dar es Salaam",
            bedrooms=3,
            description="Test description",
            has_images=True,
            user_id="USER001",
            user_account_days=100,
            user_verified=True
        )
        
        result = self.detector._check_price_anomaly(
            cheap_listing.price, cheap_listing.city, cheap_listing.bedrooms
        )
        assert result[0] > 0
        
        # Test normal price
        normal_listing = ListingRequest(
            listing_id="TEST002",
            title="Normal House",
            price=550.0,
            location="Dar es Salaam",
            city="Dar es Salaam",
            bedrooms=2,
            description="Test description",
            has_images=True,
            user_id="USER002",
            user_account_days=100,
            user_verified=True
        )
        
        result = self.detector._check_price_anomaly(
            normal_listing.price, normal_listing.city, normal_listing.bedrooms
        )
        assert result[0] < 30
    
    def test_user_behavior_analysis(self):
        """Test user behavior analysis"""
        # New user
        score, reason = self.detector._analyze_user_behavior(1, False)
        assert score >= 30
        
        # Verified user with long history
        score, reason = self.detector._analyze_user_behavior(365, True)
        assert score == 0
    
    def test_content_analysis(self):
        """Test content analysis for suspicious keywords"""
        # Suspicious content
        suspicious_desc = "URGENT! Send deposit via Western Union now!"
        score, reasons = self.detector._analyze_content(suspicious_desc, "Deal", False)
        assert score > 0
        assert len(reasons) > 0
        
        # Clean content
        clean_desc = "Beautiful apartment with sea view, secure area"
        score, reasons = self.detector._analyze_content(clean_desc, "Apartment", True)
        assert score < 50
    
    def test_location_validation(self):
        """Test location validation"""
        # Valid location
        score, reason = self.detector._validate_location("Dar es Salaam", "Masaki, Dar es Salaam")
        assert score == 0
        
        # Invalid city
        score, reason = self.detector._validate_location("Invalid City", "Some location")
        assert score > 0
    
    def test_full_analysis_legitimate(self):
        """Test complete fraud analysis for legitimate listing"""
        import asyncio
        
        legit_listing = ListingRequest(
            listing_id="LEGIT001",
            title="Modern Apartment",
            price=550.0,
            location="Masaki, Dar es Salaam",
            city="Dar es Salaam",
            bedrooms=2,
            description="Beautiful apartment with sea view",
            has_images=True,
            user_id="VERIFIED_USER",
            user_account_days=365,
            user_verified=True
        )
        
        result = asyncio.run(self.detector.analyze_listing(legit_listing))
        assert result.fraud_score < 40
    
    def test_full_analysis_fraudulent(self):
        """Test complete fraud analysis for fraudulent listing"""
        import asyncio
        
        fraud_listing = ListingRequest(
            listing_id="SCAM001",
            title="AMAZING DEAL",
            price=150.0,
            location="Somewhere",
            city="Dar es Salaam",
            bedrooms=3,
            description="URGENT! Send deposit! No viewing!",
            has_images=False,
            user_id="NEW_USER",
            user_account_days=1,
            user_verified=False
        )
        
        result = asyncio.run(self.detector.analyze_listing(fraud_listing))
        assert result.fraud_score >= 30
    
    def test_trust_score_calculation(self):
        """Test trust score calculation"""
        import asyncio
        
        user_ids = ["USER001", "USER002", "USER003"]
        for user_id in user_ids:
            result = asyncio.run(self.detector.calculate_trust_score(user_id))
            assert 0 <= result.trust_score <= 100
            assert result.user_id == user_id
            assert result.recommendation in ["APPROVE", "REVIEW", "REJECT"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])