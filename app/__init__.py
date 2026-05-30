"""
Fraud Detection & Trust Scoring System for East African Rental Market
Participant: Frank Karani | Challenge #04 | Tanzania

This package contains the complete fraud detection system with:
- Fraud detection engine (price anomaly, user behavior, content analysis)
- Trust scoring system (0-100 trust score)
- 6 detection scenarios for East African context
- REST API with FastAPI
- Web dashboard for judges
"""

__version__ = "2.0.0"
__author__ = "Frank Karani"
__participant__ = "Frank Karani"
__challenge__ = "#04 - Fraud Detection & Trust Scoring"
__region__ = "East Africa (Tanzania, Kenya, Uganda)"
__country__ = "Tanzania"

from app.config import settings

__all__ = ["settings"]