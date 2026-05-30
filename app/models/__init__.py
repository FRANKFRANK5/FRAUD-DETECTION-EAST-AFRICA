"""
Machine learning models module for Fraud Detection System
Handles model training, prediction, and serialization
Participant: Frank Karani | Challenge #04
"""

from app.models.train import train_model, evaluate_model, save_model
from app.models.predict import FraudPredictor, load_model, predict_fraud

__all__ = [
    "train_model",
    "evaluate_model",
    "save_model",
    "FraudPredictor",
    "load_model",
    "predict_fraud"
]