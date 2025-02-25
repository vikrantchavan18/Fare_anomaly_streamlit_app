import pandas as pd
import numpy as np

def process_data(df):
    """
    Process and clean the input dataframe
    """
    processed_df = df.copy()
    
    # Ensure required columns exist
    required_columns = ['fare', 'distance', 'duration']
    for col in required_columns:
        if col not in processed_df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Convert timestamp if present
    if 'timestamp' in processed_df.columns:
        processed_df['timestamp'] = pd.to_datetime(processed_df['timestamp'])
    
    # Remove null values
    processed_df = processed_df.dropna(subset=required_columns)
    
    # Remove negative values
    for col in required_columns:
        processed_df = processed_df[processed_df[col] >= 0]
    
    # Create derived features
    processed_df['fare_per_km'] = processed_df['fare'] / processed_df['distance'].clip(lower=0.1)
    processed_df['fare_per_minute'] = processed_df['fare'] / processed_df['duration'].clip(lower=1)
    
    return processed_df
