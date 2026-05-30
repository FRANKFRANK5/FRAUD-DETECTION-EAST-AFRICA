"""
Database connection module for Fraud Detection System
Handles SQLite database connections and initialization
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path("fraud_detection.db")


def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection
    
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_cursor():
    """
    Context manager for database cursor
    Automatically handles commit and close
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()


def init_db() -> None:
    """
    Initialize database tables
    Creates all required tables if they don't exist
    """
    with get_db_cursor() as cursor:
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                fraud_score INTEGER,
                trust_score INTEGER,
                risk_level TEXT,
                is_fraud BOOLEAN,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                trust_score INTEGER DEFAULT 50,
                total_listings INTEGER DEFAULT 0,
                fraud_reports INTEGER DEFAULT 0,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                listing_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT,
                price REAL,
                city TEXT,
                bedrooms INTEGER,
                has_images BOOLEAN,
                fraud_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Fraud reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fraud_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT NOT NULL,
                reporter_id TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        logger.info("Database initialized successfully")


def close_db() -> None:
    """
    Close database connection (placeholder for compatibility)
    """
    logger.info("Database connection closed")


def save_prediction_to_db(prediction_data: Dict[str, Any]) -> int:
    """
    Save prediction result to database
    
    Args:
        prediction_data: Dictionary with prediction results
        
    Returns:
        ID of inserted record
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            INSERT INTO predictions (listing_id, user_id, fraud_score, trust_score, risk_level, is_fraud)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            prediction_data.get('listing_id', ''),
            prediction_data.get('user_id', ''),
            prediction_data.get('fraud_score', 0),
            prediction_data.get('trust_score', 0),
            prediction_data.get('risk_level', ''),
            prediction_data.get('is_fraud', False)
        ))
        return cursor.lastrowid


def get_user_history(user_id: str) -> List[Dict[str, Any]]:
    """
    Get prediction history for a user
    
    Args:
        user_id: User identifier
        
    Returns:
        List of prediction records
    """
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT * FROM predictions 
            WHERE user_id = ? 
            ORDER BY prediction_date DESC 
            LIMIT 50
        ''', (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]