"""
Feature weights for fraud detection scoring
East African Rental Market - Participant: Frank Karani
"""

from typing import Dict


class FeatureWeights:
    """
    Weight distribution for different fraud detection factors
    Based on analysis of East African rental fraud patterns
    Participant: Frank Karani | Challenge #04
    """
    
    # Main factor weights (sum to 100%)
    FACTOR_WEIGHTS: Dict[str, float] = {
        "price_anomaly": 0.35,      # 35% - Most important
        "user_behavior": 0.25,       # 25% - User history
        "content_analysis": 0.20,    # 20% - Listing content
        "geographic": 0.10,          # 10% - Location validation
        "metadata": 0.10,            # 10% - Listing patterns
    }
    
    # Risk thresholds
    HIGH_RISK_THRESHOLD: float = 60.0    # >=60% = HIGH risk
    MEDIUM_RISK_THRESHOLD: float = 30.0  # 30-59% = MEDIUM risk
    # <30% = LOW risk
    
    # Trust score mapping
    TRUST_SCORE_MAPPING: Dict[str, Dict] = {
        "HIGH": {"min": 0, "max": 40, "recommendation": "REJECT"},
        "MEDIUM": {"min": 41, "max": 69, "recommendation": "REVIEW"},
        "LOW": {"min": 70, "max": 100, "recommendation": "APPROVE"},
    }
    
    # Detection scenario weights
    SCENARIO_WEIGHTS: Dict[str, float] = {
        "phantom_listing": 0.30,
        "price_anomaly": 0.25,
        "rapid_listing": 0.15,
        "identity_theft": 0.15,
        "payment_fraud": 0.10,
        "image_fraud": 0.05
    }
    
    @classmethod
    def get_risk_level(cls, fraud_score: float) -> str:
        """Determine risk level from fraud score"""
        if fraud_score >= cls.HIGH_RISK_THRESHOLD:
            return "HIGH"
        elif fraud_score >= cls.MEDIUM_RISK_THRESHOLD:
            return "MEDIUM"
        return "LOW"
    
    @classmethod
    def get_trust_recommendation(cls, trust_score: int) -> str:
        """Get recommendation based on trust score"""
        if trust_score >= 70:
            return "APPROVE"
        elif trust_score >= 50:
            return "REVIEW"
        return "REJECT"
    
    @classmethod
    def calculate_weighted_score(cls, scores: Dict[str, float]) -> float:
        """Calculate weighted score based on factor weights"""
        total = 0.0
        for factor, score in scores.items():
            if factor in cls.FACTOR_WEIGHTS:
                total += score * cls.FACTOR_WEIGHTS[factor]
        return min(100.0, max(0.0, total))