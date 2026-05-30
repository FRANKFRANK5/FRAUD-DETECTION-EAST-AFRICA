"""
Training module for Fraud Detection System
Trains machine learning model on fraud detection dataset
Participant: Frank Karani | Challenge #04 | Tanzania
"""

import joblib
import logging
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, Optional
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)   # ✅ Sahihi

def train_model(
    data_path: Optional[str] = None,
    model_path: str = "app/models/fraud_model.pkl",
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Train a fraud detection model on the dataset
    
    Args:
        data_path: Path to training data CSV file
        model_path: Path to save the trained model
        test_size: Proportion of data to use for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Dictionary with training results and metrics
    """
    
    if data_path is None or not Path(data_path).exists():
        logger.warning("No training data found. Using sample data.")
        data_path = "app/data/sample_data.csv"
    
    if not Path(data_path).exists():
        logger.warning("Sample data not found. Using synthetic data.")
        X_train, X_test, y_train, y_test = _generate_synthetic_data()
    else:
        # Load and prepare data
        df = pd.read_csv(data_path)
        X_train, X_test, y_train, y_test = _prepare_data(df, test_size, random_state)
    
    # Train Random Forest model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=random_state,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "samples_trained": len(X_train),
        "samples_tested": len(X_test)
    }
    
    # Save model
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    logger.info(f"Training metrics: {metrics}")
    
    return {
        "model": model,
        "metrics": metrics,
        "model_path": model_path
    }


def _prepare_data(
    df: pd.DataFrame,
    test_size: float,
    random_state: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Prepare data for training by selecting features and splitting
    
    Args:
        df: DataFrame with training data
        test_size: Proportion for testing
        random_state: Random seed
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    # Identify target column
    target_col = None
    for col in ['is_fraud', 'Class', 'fraud', 'label', 'target']:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        # Use last column as target
        target_col = df.columns[-1]
    
    # Select feature columns (exclude target and non-numeric)
    feature_cols = []
    for col in df.columns:
        if col != target_col:
            # Try to convert to numeric
            try:
                pd.to_numeric(df[col])
                feature_cols.append(col)
            except:
                continue
    
    if len(feature_cols) == 0:
        # Fallback: use all columns except target
        feature_cols = [col for col in df.columns if col != target_col]
    
    X = pd.get_dummies(df[feature_cols]).values
    y = df[target_col].values
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def _generate_synthetic_data(
    n_samples: int = 1000,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for demonstration
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    np.random.seed(random_state)
    
    # Generate synthetic features
    n_features = 10
    X = np.random.randn(n_samples, n_features)
    
    # Generate synthetic labels (5% fraud rate)
    y = np.zeros(n_samples)
    fraud_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    y[fraud_indices] = 1
    
    return train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """
    Evaluate a trained model on test data
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        
    Returns:
        Dictionary with evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0)
    }


def save_model(model, path: str) -> None:
    """
    Save model to disk
    
    Args:
        model: Trained model
        path: Path to save the model
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    logger.info(f"Model saved to {path}")


def load_model(path: str):
    """
    Load model from disk
    
    Args:
        path: Path to the model file
        
    Returns:
        Loaded model
    """
    return joblib.load(path)


if __name__ == "__main__":
    # Test the training function
    result = train_model()
    print(f"Training complete!")
    print(f"Metrics: {result['metrics']}")