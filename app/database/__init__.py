"""
Database module for Fraud Detection System
Handles data persistence, queries, and connection management
Participant: Frank Karani | Challenge #04
"""

from app.database.db import get_db_connection, init_db, close_db
from app.database.queries import (
    save_prediction,
    get_user_history,
    get_listing_by_id,
    get_fraud_statistics
)

__all__ = [
    "get_db_connection",
    "init_db",
    "close_db",
    "save_prediction",
    "get_user_history",
    "get_listing_by_id",
    "get_fraud_statistics"
]