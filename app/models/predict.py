"""
Prediction module for Fraud Detection System
Handles fraud prediction using trained model
Participant: Frank Karani | Challenge #04
"""

import joblib
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class FraudPredictor:
    """
    Fraud prediction class using trained machine learning model
    Participant: Frank Karani
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the predictor with optional model path
        
        Args:
            model_path: Path to the trained model file (.pkl)
        """
        self.model = None
        self.model_path = model_path or "app/models/fraud_model.pkl"
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the trained model from disk"""
        try:
            if Path(self.model_path).exists():
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded successfully from {self.model_path}")
            else:
                logger.warning(f"Model file not found at {self.model_path}. Using rule-based fallback.")
                self.model = None
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict fraud probability for given features
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(features)
        
        try:
            # Convert features to model input format
            # This is a placeholder - actual implementation depends on model
            prediction = self.model.predict([features])[0]
            probability = self.model.predict_proba([features])[0][1]
            
            return {
                "is_fraud": bool(prediction),
                "fraud_probability": float(probability),
                "confidence": float(max(probability, 1 - probability)),
                "method": "ml_model"
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return self._rule_based_prediction(features)
    
    def _rule_based_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback rule-based prediction when ML model is not available
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dictionary with prediction results
        """
        fraud_score = 0
        
        # Price anomaly
        price = features.get("price", 500)
        expected_price = features.get("expected_price", 500)
        if expected_price > 0:
            ratio = price / expected_price
            if ratio < 0.5:
                fraud_score += 35
            elif ratio > 2.0:
                fraud_score += 25
        
        # User behavior
        account_days = features.get("user_account_days", 365)
        if account_days < 7:
            fraud_score += 30
        
        if not features.get("user_verified", False):
            fraud_score += 20
        
        # Content
        if not features.get("has_images", False):
            fraud_score += 15
        
        fraud_score = min(100, fraud_score)
        
        return {
            "is_fraud": fraud_score >= 60,
            "fraud_probability": fraud_score / 100.0,
            "confidence": 0.70,
            "method": "rule_based_fallback"
        }


def load_model(model_path: Optional[str] = None) -> FraudPredictor:
    """
    Convenience function to load the fraud predictor
    
    Args:
        model_path: Optional path to model file
        
    Returns:
        FraudPredictor instance
    """
    return FraudPredictor(model_path)


def predict_fraud(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Quick prediction function for fraud detection
    
    Args:
        features: Dictionary of feature values
        
    Returns:
        Dictionary with prediction results
    """
    predictor = FraudPredictor()
    return predictor.predict(features)