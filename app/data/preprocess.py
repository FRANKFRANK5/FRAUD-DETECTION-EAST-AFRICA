"""
Data preprocessing module for Fraud Detection System
Cleans and prepares data for fraud detection
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import re
import pandas as pd
from typing import Dict, Any, Optional


def preprocess_listing_data(listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess listing data before feature extraction
    
    Args:
        listing_data: Raw listing data dictionary
        
    Returns:
        Cleaned listing data dictionary
    """
    cleaned = {}
    
    # Clean listing_id
    cleaned['listing_id'] = clean_text(listing_data.get('listing_id', ''))[:50]
    
    # Clean title
    cleaned['title'] = clean_text(listing_data.get('title', ''))[:200]
    
    # Clean description
    cleaned['description'] = clean_text(listing_data.get('description', ''))[:5000]
    
    # Clean location
    cleaned['location'] = clean_text(listing_data.get('location', ''))[:500]
    
    # Clean city
    cleaned['city'] = clean_city_name(listing_data.get('city', ''))
    
    # Normalize price
    cleaned['price'] = normalize_price(listing_data.get('price', 0))
    
    # Validate bedrooms
    cleaned['bedrooms'] = validate_bedrooms(listing_data.get('bedrooms', 1))
    
    # Boolean fields
    cleaned['has_images'] = bool(listing_data.get('has_images', False))
    cleaned['user_verified'] = bool(listing_data.get('user_verified', False))
    
    # User fields
    cleaned['user_id'] = clean_text(listing_data.get('user_id', ''))[:100]
    cleaned['user_account_days'] = validate_account_days(listing_data.get('user_account_days', 0))
    
    return cleaned


def clean_text(text: str) -> str:
    """
    Clean text by removing special characters and extra spaces
    
    Args:
        text: Input text string
        
    Returns:
        Cleaned text string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (keep letters, numbers, spaces, basic punctuation)
    text = re.sub(r'[^\w\s\-\.\,\!\\?]', '', text)
    
    # Strip leading/trailing spaces
    text = text.strip()
    
    return text


def normalize_price(price: Any) -> float:
    """
    Normalize price to valid range
    
    Args:
        price: Input price value
        
    Returns:
        Normalized price between 50 and 10000
    """
    try:
        price_float = float(price)
    except (ValueError, TypeError):
        price_float = 500.0
    
    # Cap at reasonable range for East Africa
    if price_float < 50:
        return 50.0
    if price_float > 10000:
        return 10000.0
    
    return round(price_float, 2)


def clean_city_name(city: str) -> str:
    """
    Clean and standardize city name
    
    Args:
        city: Input city name
        
    Returns:
        Standardized city name
    """
    if not city or not isinstance(city, str):
        return "Unknown"
    
    city_lower = city.lower().strip()
    
    # City name mapping
    city_mapping = {
        "dar": "Dar es Salaam", "dar es": "Dar es Salaam", "dsm": "Dar es Salaam",
        "nrb": "Nairobi", "nairob": "Nairobi",
        "kla": "Kampala", "kampal": "Kampala",
        "arush": "Arusha",
        "mombas": "Mombasa",
        "zanzibar": "Zanzibar", "znz": "Zanzibar"
    }
    
    for key, value in city_mapping.items():
        if key in city_lower:
            return value
    
    # Capitalize first letter of each word
    return city.title()


def validate_bedrooms(bedrooms: Any) -> int:
    """
    Validate bedrooms value
    
    Args:
        bedrooms: Input bedrooms value
        
    Returns:
        Validated bedrooms (0-10)
    """
    try:
        beds = int(bedrooms)
    except (ValueError, TypeError):
        beds = 1
    
    if beds < 0:
        return 0
    if beds > 10:
        return 10
    
    return beds


def validate_account_days(days: Any) -> int:
    """
    Validate account age in days
    
    Args:
        days: Input days value
        
    Returns:
        Validated days (0-3650)
    """
    try:
        account_days = int(days)
    except (ValueError, TypeError):
        account_days = 30
    
    if account_days < 0:
        return 0
    if account_days > 3650:
        return 3650
    
    return account_days


def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess entire dataset DataFrame
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Clean text columns if they exist
    text_columns = ['title', 'description', 'location']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(lambda x: clean_text(str(x)))
    
    # Clean city column
    if 'city' in df_clean.columns:
        df_clean['city'] = df_clean['city'].apply(clean_city_name)
    
    # Normalize price
    if 'price' in df_clean.columns:
        df_clean['price'] = df_clean['price'].apply(normalize_price)
    
    return df_clean