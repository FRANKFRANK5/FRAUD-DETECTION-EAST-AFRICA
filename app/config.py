"""
Configuration settings for Fraud Detection System
East African Rental Market - Hackathon Challenge #04
Participant: Frank Karani | Tanzania
"""

from typing import List, Dict


class Settings:
    """Application configuration settings"""
    
    # Application info
    APP_NAME: str = "Fraud Detection & Trust Scoring API"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Participant info
    PARTICIPANT_NAME: str = "Frank Karani"
    COUNTRY: str = "Tanzania"
    CHALLENGE: str = "#04 - Fraud Detection & Trust Scoring"
    
    # Security - CORS allowed origins
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://*.onrender.com",
        "https://*.railway.app"
    ]
    
    # Security - Trusted hosts
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "*.onrender.com",
        "*.railway.app"
    ]
    
    # Fraud detection thresholds
    HIGH_RISK_THRESHOLD: float = 60.0
    MEDIUM_RISK_THRESHOLD: float = 30.0
    
    # Trust score thresholds
    TRUST_HIGH_THRESHOLD: int = 70
    TRUST_MEDIUM_THRESHOLD: int = 50
    
    # East African market data
    EA_COUNTRIES: List[str] = ["Tanzania", "Kenya", "Uganda"]
    
    EA_CITIES: Dict[str, List[str]] = {
        "Tanzania": ["Dar es Salaam", "Arusha", "Mwanza", "Zanzibar", "Dodoma", "Mbeya", "Tanga"],
        "Kenya": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi"],
        "Uganda": ["Kampala", "Entebbe", "Jinja", "Gulu", "Mbarara", "Mbale"]
    }
    
    # Currency
    CURRENCY: str = "USD"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Rate limiting (requests per minute)
    RATE_LIMIT_DEFAULT: int = 100
    RATE_LIMIT_DETECTION: int = 50
    RATE_LIMIT_TRUST_SCORE: int = 100


# Create global settings instance
settings = Settings()