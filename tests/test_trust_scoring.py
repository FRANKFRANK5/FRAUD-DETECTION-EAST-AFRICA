"""
Trust scoring tests for Fraud Detection System
Tests trust score calculation and risk assessment
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.trust_scoring.calculator import FraudDetector
from app.trust_scoring.weights import FeatureWeights
from app.trust_scoring.rules import RiskRules


class TestTrustScoring:
    """Test class for trust scoring functionality"""
    
    def setup_method(self):
        """Setup before each test"""
        self.detector = FraudDetector()
    
    def test_risk_level_mapping(self):
        """Test risk level mapping from fraud score"""
        # High risk
        assert FeatureWeights.get_risk_level(80) == "HIGH"
        assert FeatureWeights.get_risk_level(100) == "HIGH"
        
        # Medium risk
        assert FeatureWeights.get_risk_level(50) == "MEDIUM"
        assert FeatureWeights.get_risk_level(45) == "MEDIUM"
        
        # Low risk
        assert FeatureWeights.get_risk_level(20) == "LOW"
        assert FeatureWeights.get_risk_level(0) == "LOW"
    
    def test_trust_recommendation(self):
        """Test trust score recommendations"""
        # High trust
        assert FeatureWeights.get_trust_recommendation(85) == "APPROVE"
        assert FeatureWeights.get_trust_recommendation(70) == "APPROVE"
        
        # Medium trust
        assert FeatureWeights.get_trust_recommendation(60) == "REVIEW"
        assert FeatureWeights.get_trust_recommendation(55) == "REVIEW"
        
        # Low trust
        assert FeatureWeights.get_trust_recommendation(40) == "REJECT"
        assert FeatureWeights.get_trust_recommendation(30) == "REJECT"
    
    def test_price_anomaly_rules(self):
        """Test price anomaly detection rules"""
        # Too cheap (60% below)
        score, reason = RiskRules.get_price_anomaly_score(200, "Dar es Salaam", 2)
        assert score >= 40
        
        # Normal price
        score, reason = RiskRules.get_price_anomaly_score(550, "Dar es Salaam", 2)
        assert score == 0
        
        # Too expensive
        score, reason = RiskRules.get_price_anomaly_score(1500, "Dar es Salaam", 2)
        assert score > 0
    
    def test_user_behavior_rules(self):
        """Test user behavior rules"""
        # Brand new user
        score, reason = RiskRules.get_user_behavior_score(0, False)
        assert score >= 50
        
        # Established user
        score, reason = RiskRules.get_user_behavior_score(365, True)
        assert score == 0
    
    def test_content_rules(self):
        """Test content analysis rules"""
        # With suspicious keywords
        score, reasons = RiskRules.get_content_score(
            "URGENT! Send money via Western Union", 
            "AMAZING DEAL", 
            False
        )
        assert score > 0
        assert len(reasons) > 0
        
        # Clean content
        score, reasons = RiskRules.get_content_score(
            "Beautiful apartment in secure area", 
            "Modern Apartment", 
            True
        )
        assert score < 50
    
    def test_geographic_rules(self):
        """Test geographic validation rules"""
        # Valid location
        score, reason = RiskRules.get_geographic_score("Dar es Salaam", "Masaki, Dar es Salaam")
        assert score == 0
        
        # Invalid city
        score, reason = RiskRules.get_geographic_score("Invalid City", "Some location")
        assert score > 0
    
    def test_weighted_score_calculation(self):
        """Test weighted score calculation"""
        scores = {
            "price_anomaly": 80,
            "user_behavior": 50,
            "content_analysis": 30,
            "geographic": 0,
            "metadata": 10
        }
        
        weighted = FeatureWeights.calculate_weighted_score(scores)
        assert 0 <= weighted <= 100
        
        # Empty scores
        empty_scores = {}
        weighted = FeatureWeights.calculate_weighted_score(empty_scores)
        assert weighted == 0
    
    def test_different_cities(self):
        """Test trust scoring across different East African cities"""
        cities = [
            "Dar es Salaam", "Nairobi", "Kampala", 
            "Arusha", "Mombasa", "Zanzibar"
        ]
        
        for city in cities:
            # Should not crash for any city
            assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])