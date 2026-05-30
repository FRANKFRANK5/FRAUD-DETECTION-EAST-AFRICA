"""
Fraud Detection Engine for East African Rental Market
Participant: Frank Karani | Challenge #04 | Tanzania

Implements multiple detection strategies:
1. Price anomaly detection (35% weight)
2. User behavior analysis (25% weight)
3. Content analysis (20% weight)
4. Geographic validation (10% weight)
5. Listing metadata analysis (10% weight)
"""

import hashlib
import logging
from typing import Dict, List, Tuple
from app.api.schemas import ListingRequest, FraudResponse, TrustScoreResponse

logger = logging.getLogger(__name__)


class FraudDetector:
    """
    Main fraud detection engine with multi-factor analysis
    Participant: Frank Karani
    """
    
    # East African market price database (USD per month)
    MARKET_PRICES: Dict[str, Dict[str, float]] = {
        "dar es salaam": {"1": 350, "2": 550, "3": 800, "4": 1200},
        "nairobi": {"1": 400, "2": 650, "3": 950, "4": 1400},
        "kampala": {"1": 300, "2": 500, "3": 750, "4": 1100},
        "arusha": {"1": 250, "2": 400, "3": 600, "4": 900},
        "mombasa": {"1": 300, "2": 500, "3": 700, "4": 1000},
        "zanzibar": {"1": 400, "2": 650, "3": 1000, "4": 1500},
        "kisumu": {"1": 250, "2": 400, "3": 600, "4": 850},
        "mwanza": {"1": 200, "2": 350, "3": 500, "4": 750},
        "dodoma": {"1": 200, "2": 350, "3": 500, "4": 750},
        "eldoret": {"1": 200, "2": 350, "3": 500, "4": 750}
    }
    
    # Suspicious keywords with fraud weight
    SUSPICIOUS_KEYWORDS: Dict[str, int] = {
        "urgent": 15, "deposit": 20, "western union": 30,
        "moneygram": 30, "overseas": 15, "agent fee": 25,
        "refundable": 10, "bitcoin": 35, "send money": 25,
        "no viewing": 40, "out of country": 30, "haraka": 15,
        "amana": 20, "tuma pesa": 25, "nje ya nchi": 30
    }
    
    # Valid East African cities (lowercase and title case for frontend compatibility)
    VALID_CITIES = {
        "dar es salaam", "nairobi", "kampala", "arusha", "mombasa",
        "zanzibar", "kisumu", "mwanza", "dodoma", "eldoret",
        "jinja", "gulu", "mbale", "nakuru", "thika",
        "Dar es Salaam", "Nairobi", "Kampala", "Arusha", "Mombasa",
        "Zanzibar", "Kisumu", "Mwanza", "Dodoma", "Eldoret"
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def analyze_listing(self, listing: ListingRequest) -> FraudResponse:
        """
        Comprehensive fraud analysis for a rental listing
        Analyzes multiple factors and returns weighted fraud score
        """
        fraud_score = 0.0
        reasons = []
        
        # Factor 1: Price anomaly detection (35% weight)
        price_score, price_reason = self._check_price_anomaly(
            listing.price, listing.city, listing.bedrooms
        )
        fraud_score += price_score * 0.35
        if price_reason:
            reasons.append(price_reason)
        
        # Factor 2: User behavior analysis (25% weight)
        user_score, user_reason = self._analyze_user_behavior(
            listing.user_account_days, listing.user_verified
        )
        fraud_score += user_score * 0.25
        if user_reason:
            reasons.append(user_reason)
        
        # Factor 3: Content analysis (20% weight)
        content_score, content_reasons = self._analyze_content(
            listing.description, listing.title, listing.has_images
        )
        fraud_score += content_score * 0.20
        reasons.extend(content_reasons)
        
        # Factor 4: Geographic validation (10% weight)
        geo_score, geo_reason = self._validate_location(listing.city, listing.location)
        fraud_score += geo_score * 0.10
        if geo_reason:
            reasons.append(geo_reason)
        
        # Factor 5: Listing metadata analysis (10% weight)
        metadata_score, metadata_reasons = self._analyze_listing_metadata(listing)
        fraud_score += metadata_score * 0.10
        reasons.extend(metadata_reasons)
        
        # Normalize fraud score to 0-100
        fraud_score = min(100.0, max(0.0, fraud_score))
        
        # Calculate trust score (inverse of fraud score)
        trust_score = int(100 - fraud_score)
        
        # Determine risk level
        if fraud_score >= 60:
            risk_level = "HIGH"
            is_fraud = True
        elif fraud_score >= 30:
            risk_level = "MEDIUM"
            is_fraud = False
        else:
            risk_level = "LOW"
            is_fraud = False
        
        # Remove duplicate reasons and limit to 5
        unique_reasons = list(dict.fromkeys(reasons))[:5]
        
        return FraudResponse(
            is_fraud=is_fraud,
            fraud_score=int(fraud_score),
            risk_level=risk_level,
            reasons=unique_reasons,
            trust_score=trust_score
        )
    
    async def calculate_trust_score(self, user_id: str) -> TrustScoreResponse:
        """
        Calculate trust score for a user based on deterministic hash
        In production, this would query a database with historical data
        """
        # Create deterministic but varied score based on user_id
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
        trust_score = 40 + (hash_val % 55)  # Range: 40-94
        
        if trust_score >= 70:
            risk_level = "LOW"
            recommendation = "APPROVE"
        elif trust_score >= 50:
            risk_level = "MEDIUM"
            recommendation = "REVIEW"
        else:
            risk_level = "HIGH"
            recommendation = "REJECT"
        
        return TrustScoreResponse(
            user_id=user_id,
            trust_score=trust_score,
            risk_level=risk_level,
            recommendation=recommendation
        )
    
    def _check_price_anomaly(self, price: float, city: str, bedrooms: int) -> Tuple[float, str]:
        """Detect price anomalies against market averages"""
        city_key = city.lower()
        bed_key = str(bedrooms)
        
        if city_key in self.MARKET_PRICES:
            expected = self.MARKET_PRICES[city_key].get(bed_key, 500)
            ratio = price / expected if expected > 0 else 1
            
            if ratio < 0.4:
                return 100.0, f"💰 Price is 60% below market for {city} - Classic phantom listing"
            elif ratio < 0.6:
                return 70.0, f"💰 Price {int((1-ratio)*100)}% below market - Suspiciously cheap"
            elif ratio < 0.8:
                return 40.0, f"💰 Price {int((1-ratio)*100)}% below market average"
            elif ratio > 2.5:
                return 80.0, f"💰 Price 150% above market - Potential luxury scam"
            elif ratio > 1.8:
                return 50.0, f"💰 Price {int((ratio-1)*100)}% above market average"
        
        return 0.0, ""
    
    def _analyze_user_behavior(self, account_age_days: int, is_verified: bool) -> Tuple[float, str]:
        """Analyze user behavior patterns for fraud indicators"""
        if account_age_days < 1:
            return 80.0, "👤 Brand new account (less than 24 hours) - High risk"
        elif account_age_days < 7:
            return 50.0, "👤 New account (less than 7 days)"
        elif account_age_days < 30:
            return 20.0, "👤 Recent account (less than 30 days)"
        
        if not is_verified:
            return 40.0, "🔓 Unverified user - No identity confirmation"
        
        return 0.0, ""
    
    def _analyze_content(self, description: str, title: str, has_images: bool) -> Tuple[float, List[str]]:
        """Analyze listing content for fraud indicators"""
        score = 0.0
        reasons = []
        combined_text = f"{title} {description}".lower()
        
        # Check for suspicious keywords
        for keyword, weight in self.SUSPICIOUS_KEYWORDS.items():
            if keyword in combined_text:
                score += weight * 0.6
                reasons.append(f"⚠️ Suspicious keyword: '{keyword}'")
                break
        
        if not has_images:
            score += 35.0
            reasons.append("📷 No images provided - Common in phantom listings")
        
        if len(description.strip()) < 50:
            score += 15.0
            reasons.append("📝 Very short description - Lacks detail")
        
        return min(100.0, score), reasons
    
    def _validate_location(self, city: str, location: str) -> Tuple[float, str]:
        """Validate geographic information for East Africa"""
        city_key = city.lower()
        
        if city_key not in self.VALID_CITIES:
            return 60.0, f"🌍 City '{city}' not recognized in East Africa"
        
        if len(location.strip()) < 15:
            return 30.0, "📍 Vague location - No specific address"
        
        return 0.0, ""
    
    def _analyze_listing_metadata(self, listing: ListingRequest) -> Tuple[float, List[str]]:
        """Analyze listing metadata for fraud patterns"""
        score = 0.0
        reasons = []
        
        if listing.price < 100 and listing.bedrooms >= 2:
            score += 50.0
            reasons.append("💸 Extremely low price for multi-bedroom unit")
        
        if len(listing.listing_id) < 3 or not listing.listing_id[0].isalpha():
            score += 15.0
            reasons.append("🔖 Invalid listing ID format")
        
        return min(100.0, score), reasons