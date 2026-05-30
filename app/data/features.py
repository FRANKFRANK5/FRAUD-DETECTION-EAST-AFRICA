"""
Feature engineering module for Fraud Detection System
Extracts and transforms features for fraud detection
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import re
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime


class FeatureExtractor:
    """
    Extract and engineer features from listing data
    Participant: Frank Karani
    """
    
    def __init__(self):
        self.suspicious_keywords = [
            "urgent", "deposit", "western union", "moneygram",
            "overseas", "agent fee", "refundable", "bitcoin",
            "send money", "no viewing", "out of country"
        ]
    
    def extract_all_features(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract all features from listing data
        
        Args:
            listing_data: Dictionary containing listing information
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Price features
        features['price'] = listing_data.get('price', 0)
        features['price_per_bedroom'] = self._calc_price_per_bedroom(listing_data)
        
        # Text features
        features['title_length'] = len(listing_data.get('title', ''))
        features['description_length'] = len(listing_data.get('description', ''))
        features['has_suspicious_keywords'] = self._check_suspicious_keywords(listing_data)
        features['suspicious_keyword_count'] = self._count_suspicious_keywords(listing_data)
        
        # User features
        features['account_age_days'] = listing_data.get('user_account_days', 0)
        features['is_verified'] = 1 if listing_data.get('user_verified', False) else 0
        features['is_new_account'] = 1 if features['account_age_days'] < 7 else 0
        
        # Listing features
        features['has_images'] = 1 if listing_data.get('has_images', False) else 0
        features['bedrooms'] = listing_data.get('bedrooms', 0)
        features['listing_id_length'] = len(listing_data.get('listing_id', ''))
        
        # Location features
        features['city_known'] = 1 if self._is_valid_city(listing_data.get('city', '')) else 0
        features['location_specific'] = 1 if len(listing_data.get('location', '')) > 20 else 0
        
        return features
    
    def create_feature_vector(self, listing_data: Dict[str, Any]) -> np.ndarray:
        """
        Create numpy feature vector for model input
        
        Args:
            listing_data: Dictionary containing listing information
            
        Returns:
            Numpy array of feature values
        """
        features = self.extract_all_features(listing_data)
        
        # Order matters for model consistency
        feature_order = [
            'price', 'price_per_bedroom', 'title_length', 'description_length',
            'has_suspicious_keywords', 'suspicious_keyword_count', 'account_age_days',
            'is_verified', 'is_new_account', 'has_images', 'bedrooms',
            'listing_id_length', 'city_known', 'location_specific'
        ]
        
        return np.array([features[f] for f in feature_order if f in features], dtype=np.float32)
    
    def _calc_price_per_bedroom(self, listing_data: Dict[str, Any]) -> float:
        """Calculate price per bedroom"""
        price = listing_data.get('price', 0)
        bedrooms = listing_data.get('bedrooms', 1)
        if bedrooms > 0:
            return price / bedrooms
        return price
    
    def _check_suspicious_keywords(self, listing_data: Dict[str, Any]) -> int:
        """Check if listing contains suspicious keywords"""
        text = f"{listing_data.get('title', '')} {listing_data.get('description', '')}".lower()
        for keyword in self.suspicious_keywords:
            if keyword in text:
                return 1
        return 0
    
    def _count_suspicious_keywords(self, listing_data: Dict[str, Any]) -> int:
        """Count number of suspicious keywords in listing"""
        text = f"{listing_data.get('title', '')} {listing_data.get('description', '')}".lower()
        count = 0
        for keyword in self.suspicious_keywords:
            if keyword in text:
                count += 1
        return min(count, 5)
    
    def _is_valid_city(self, city: str) -> bool:
        """Check if city is a valid East African city"""
        valid_cities = {
            "dar es salaam", "nairobi", "kampala", "arusha", "mombasa",
            "zanzibar", "kisumu", "mwanza", "dodoma", "eldoret"
        }
        return city.lower() in valid_cities


def extract_features(listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to extract features
    
    Args:
        listing_data: Dictionary containing listing information
        
    Returns:
        Dictionary of extracted features
    """
    extractor = FeatureExtractor()
    return extractor.extract_all_features(listing_data)


def create_feature_vector(listing_data: Dict[str, Any]) -> np.ndarray:
    """
    Convenience function to create feature vector
    
    Args:
        listing_data: Dictionary containing listing information
        
    Returns:
        Numpy array of feature values
    """
    extractor = FeatureExtractor()
    return extractor.create_feature_vector(listing_data)