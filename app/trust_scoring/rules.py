"""
Risk rules for East African rental market fraud detection
Participant: Frank Karani | Challenge #04
"""

from typing import Dict, List, Tuple


class RiskRules:
    """
    Collection of fraud detection rules for East African rental market
    Participant: Frank Karani
    """
    
    # Suspicious keywords (English & Swahili for East Africa)
    SUSPICIOUS_KEYWORDS: Dict[str, int] = {
        # English
        "urgent": 15, "deposit": 20, "western union": 30,
        "moneygram": 30, "overseas": 15, "agent fee": 25,
        "refundable": 10, "bitcoin": 35, "send money": 25,
        "no viewing": 40, "out of country": 30, "advance payment": 25,
        # Swahili (East African context)
        "haraka": 15, "amana": 20, "tuma pesa": 25,
        "nje ya nchi": 30, "wakala": 20, "pesa ya mbele": 25
    }
    
    # Market prices by city (USD per month)
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
    
    @classmethod
    def get_price_anomaly_score(cls, price: float, city: str, bedrooms: int) -> Tuple[float, str]:
        """Calculate price anomaly score based on East African market data"""
        city_key = city.lower()
        bed_key = str(bedrooms)
        
        if city_key in cls.MARKET_PRICES:
            expected = cls.MARKET_PRICES[city_key].get(bed_key, 500)
            ratio = price / expected if expected > 0 else 1
            
            if ratio < 0.4:
                return 100.0, f"Price 60% below market for {city}"
            elif ratio < 0.6:
                return 70.0, f"Price {int((1-ratio)*100)}% below market"
            elif ratio < 0.8:
                return 40.0, f"Price {int((1-ratio)*100)}% below market"
            elif ratio > 2.5:
                return 80.0, f"Price 150% above market for {city}"
            elif ratio > 1.8:
                return 50.0, f"Price {int((ratio-1)*100)}% above market"
        
        return 0.0, ""
    
    @classmethod
    def get_user_behavior_score(cls, account_days: int, is_verified: bool) -> Tuple[float, str]:
        """Calculate user behavior risk score"""
        if account_days < 1:
            return 80.0, "Brand new account (less than 24 hours)"
        elif account_days < 7:
            return 50.0, "New account (less than 7 days)"
        elif account_days < 30:
            return 20.0, "Recent account (less than 30 days)"
        
        if not is_verified:
            return 40.0, "Unverified user account"
        
        return 0.0, ""
    
    @classmethod
    def get_content_score(cls, description: str, title: str, has_images: bool) -> Tuple[float, List[str]]:
        """Calculate content risk score"""
        score = 0.0
        reasons = []
        combined = f"{title} {description}".lower()
        
        # Check suspicious keywords
        for keyword, weight in cls.SUSPICIOUS_KEYWORDS.items():
            if keyword in combined:
                score += weight
                reasons.append(f"Suspicious keyword: '{keyword}'")
                break
        
        # Check images
        if not has_images:
            score += 35.0
            reasons.append("No images provided")
        
        # Check description length
        if len(description.strip()) < 50:
            score += 15.0
            reasons.append("Very short description")
        
        return min(100.0, score), reasons[:3]
    
    @classmethod
    def get_geographic_score(cls, city: str, location: str) -> Tuple[float, str]:
        """Calculate geographic validation score"""
        valid_cities = {
            "dar es salaam", "nairobi", "kampala", "arusha", "mombasa",
            "zanzibar", "kisumu", "mwanza", "dodoma", "eldoret"
        }
        
        if city.lower() not in valid_cities:
            return 60.0, f"City '{city}' not recognized"
        
        if len(location.strip()) < 15:
            return 30.0, "Vague location description"
        
        return 0.0, ""