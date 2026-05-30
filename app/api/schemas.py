"""
Pydantic schemas for request/response validation
Implements input validation to prevent injection attacks
Participant: Frank Karani | Challenge #04
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ListingRequest(BaseModel):
    """
    Request schema for fraud detection endpoint
    All fields are validated to prevent injection attacks
    """
    
    listing_id: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="Unique identifier for the listing",
        examples=["LST-2024-001"]
    )
    
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Listing title",
        examples=["Spacious 2BR Apartment in Dar es Salaam"]
    )
    
    price: float = Field(
        ...,
        gt=0,
        le=100000,
        description="Monthly rent in USD",
        examples=[550.0]
    )
    
    location: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Full location description",
        examples=["Masaki, Dar es Salaam, Tanzania"]
    )
    
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="City name",
        examples=["Dar es Salaam"]
    )
    
    bedrooms: int = Field(
        ...,
        ge=0,
        le=10,
        description="Number of bedrooms",
        examples=[2]
    )
    
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Full listing description",
        examples=["Modern apartment with sea view..."]
    )
    
    has_images: bool = Field(
        default=False,
        description="Whether the listing has images"
    )
    
    user_id: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="User identifier",
        examples=["USER_12345"]
    )
    
    user_account_days: int = Field(
        ...,
        ge=0,
        le=3650,
        description="User account age in days",
        examples=[365]
    )
    
    user_verified: bool = Field(
        default=False,
        description="Whether user identity is verified"
    )
    
    @field_validator('title', 'description', 'location')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Remove leading/trailing whitespace"""
        return v.strip() if v else v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        """Validate price is reasonable for East African market"""
        if v < 50:
            raise ValueError("Price below $50 is unrealistic for East African rental market")
        if v > 50000:
            raise ValueError("Price above $50,000 exceeds reasonable range")
        return round(v, 2)
    
    @field_validator('city')
    @classmethod
    def validate_city(cls, v: str) -> str:
        """Validate city name against East African cities"""
        v = v.strip().lower()
        valid_cities = [
            "dar es salaam", "nairobi", "kampala", "arusha", "mombasa",
            "zanzibar", "kisumu", "mwanza", "dodoma", "eldoret",
            "jinja", "gulu", "mbale", "nakuru", "thika"
        ]
        if v not in valid_cities:
            raise ValueError(f"City '{v}' not recognized. Valid cities: {', '.join(valid_cities)}")
        return v.title()
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user ID format to prevent injection"""
        import re
        if not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError("User ID must contain only alphanumeric characters, underscores, and hyphens")
        return v


class FraudResponse(BaseModel):
    """Response schema for fraud detection"""
    
    is_fraud: bool = Field(
        ...,
        description="Whether the listing is classified as fraudulent"
    )
    
    fraud_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Fraud probability score (0-100)"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level: LOW, MEDIUM, or HIGH"
    )
    
    reasons: List[str] = Field(
        default_factory=list,
        description="List of reasons for the fraud classification",
        max_length=10
    )
    
    trust_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Associated trust score for the user"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_fraud": False,
                "fraud_score": 15,
                "risk_level": "LOW",
                "reasons": ["Price slightly below market average"],
                "trust_score": 85
            }
        }


class TrustScoreResponse(BaseModel):
    """Response schema for trust score endpoint"""
    
    user_id: str = Field(..., description="User identifier")
    
    trust_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Trust score (0-100)"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level: LOW, MEDIUM, or HIGH"
    )
    
    recommendation: str = Field(
        ...,
        description="Recommended action: APPROVE, REVIEW, or REJECT"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "USER_12345",
                "trust_score": 85,
                "risk_level": "LOW",
                "recommendation": "APPROVE"
            }
        }


class HealthResponse(BaseModel):
    """Health check response schema"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    service: str = Field(..., description="Service name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0.0",
                "service": "fraud-detection-api"
            }
        }


class DetectionScenario(BaseModel):
    """Detection scenario schema for judges"""
    
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    indicators: List[str] = Field(..., description="Fraud indicators")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Phantom Listing",
                "description": "Listing doesn't physically exist",
                "indicators": ["Too cheap", "No images", "New user"]
            }
        }