"""
Database queries module for Fraud Detection System
Contains all database query operations
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import logging
from typing import Dict, Any, List, Optional
from app.database.db import get_db_cursor

logger = logging.getLogger(__name__)


def save_prediction(
    listing_id: str,
    user_id: str,
    fraud_score: int,
    trust_score: int,
    risk_level: str,
    is_fraud: bool
) -> int:
    """
    Save a fraud prediction to the database
    
    Args:
        listing_id: Listing identifier
        user_id: User identifier
        fraud_score: Fraud score (0-100)
        trust_score: Trust score (0-100)
        risk_level: Risk level (LOW/MEDIUM/HIGH)
        is_fraud: Whether listing is fraudulent
        
    Returns:
        ID of inserted record
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            INSERT INTO predictions (listing_id, user_id, fraud_score, trust_score, risk_level, is_fraud)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (listing_id, user_id, fraud_score, trust_score, risk_level, is_fraud))
        
        # Update user's total listings
        cursor.execute('''
            INSERT INTO users (user_id, total_listings) 
            VALUES (?, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                total_listings = total_listings + 1
        ''', (user_id,))
        
        return cursor.lastrowid


def get_user_history(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get prediction history for a specific user
    
    Args:
        user_id: User identifier
        limit: Maximum number of records to return
        
    Returns:
        List of prediction records
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT listing_id, fraud_score, trust_score, risk_level, is_fraud, prediction_date
            FROM predictions 
            WHERE user_id = ? 
            ORDER BY prediction_date DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        return [dict(row) for row in cursor.fetchall()]


def get_listing_by_id(listing_id: str) -> Optional[Dict[str, Any]]:
    """
    Get listing information by ID
    
    Args:
        listing_id: Listing identifier
        
    Returns:
        Listing record or None if not found
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT l.*, u.trust_score as user_trust_score
            FROM listings l
            LEFT JOIN users u ON l.user_id = u.user_id
            WHERE l.listing_id = ?
        ''', (listing_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None


def get_fraud_statistics() -> Dict[str, Any]:
    """
    Get overall fraud detection statistics
    
    Returns:
        Dictionary with statistics
    """
    with get_db_cursor() as cursor:
        # Total predictions
        cursor.execute("SELECT COUNT(*) as total FROM predictions")
        total = cursor.fetchone()['total']
        
        # Fraud count
        cursor.execute("SELECT COUNT(*) as fraud_count FROM predictions WHERE is_fraud = 1")
        fraud_count = cursor.fetchone()['fraud_count']
        
        # Average scores
        cursor.execute("SELECT AVG(fraud_score) as avg_fraud, AVG(trust_score) as avg_trust FROM predictions")
        avg_row = cursor.fetchone()
        
        # High risk count
        cursor.execute("SELECT COUNT(*) as high_risk FROM predictions WHERE risk_level = 'HIGH'")
        high_risk = cursor.fetchone()['high_risk']
        
        return {
            "total_predictions": total,
            "fraud_detected": fraud_count,
            "fraud_rate": round(fraud_count / total * 100, 2) if total > 0 else 0,
            "avg_fraud_score": round(avg_row['avg_fraud'], 2) if avg_row['avg_fraud'] else 0,
            "avg_trust_score": round(avg_row['avg_trust'], 2) if avg_row['avg_trust'] else 0,
            "high_risk_listings": high_risk
        }


def update_user_trust_score(user_id: str, new_trust_score: int) -> bool:
    """
    Update a user's trust score
    
    Args:
        user_id: User identifier
        new_trust_score: New trust score (0-100)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute('''
                UPDATE users SET trust_score = ? WHERE user_id = ?
            ''', (new_trust_score, user_id))
            
            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT INTO users (user_id, trust_score) VALUES (?, ?)
                ''', (user_id, new_trust_score))
            
            return True
    except Exception as e:
        logger.error(f"Error updating trust score: {str(e)}")
        return False


def report_fraud(listing_id: str, reporter_id: str, reason: str) -> int:
    """
    Report a listing as fraudulent
    
    Args:
        listing_id: Listing identifier
        reporter_id: User reporting the fraud
        reason: Reason for reporting
        
    Returns:
        ID of inserted report
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            INSERT INTO fraud_reports (listing_id, reporter_id, reason)
            VALUES (?, ?, ?)
        ''', (listing_id, reporter_id, reason))
        
        # Update fraud reports count for the listing's user
        cursor.execute('''
            UPDATE users SET fraud_reports = fraud_reports + 1
            WHERE user_id = (SELECT user_id FROM listings WHERE listing_id = ?)
        ''', (listing_id,))
        
        return cursor.lastrowid