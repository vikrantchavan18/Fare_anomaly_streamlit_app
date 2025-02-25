from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

def detect_anomalies(df, contamination=0.1):
    """
    Detect anomalies using Isolation Forest
    """
    # Select features for anomaly detection
    features = ['fare', 'distance', 'duration', 'fare_per_km', 'fare_per_minute']
    X = df[features]
    
    # Initialize and fit the Isolation Forest model
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    
    # Fit and predict
    predictions = iso_forest.fit_predict(X)
    
    # Add predictions to dataframe (1: normal, -1: anomaly)
    df_with_anomalies = df.copy()
    df_with_anomalies['is_anomaly'] = predictions == -1
    
    # Calculate anomaly scores
    scores = iso_forest.score_samples(X)
    df_with_anomalies['anomaly_score'] = scores
    
    return df_with_anomalies
