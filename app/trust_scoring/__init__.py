"""
Trust Scoring module for Fraud Detection System
Handles fraud detection, risk scoring, and trust calculation
Participant: Frank Karani | Challenge #04
"""

from app.trust_scoring.calculator import FraudDetector, calculate_risk_score
from app.trust_scoring.rules import RiskRules, get_price_anomaly_score, get_user_behavior_score
from app.trust_scoring.weights import FeatureWeights, get_risk_level, get_trust_recommendation

__all__ = [
    "FraudDetector",
    "calculate_risk_score",
    "RiskRules",
    "get_price_anomaly_score",
    "get_user_behavior_score",
    "FeatureWeights",
    "get_risk_level",
    "get_trust_recommendation"
]