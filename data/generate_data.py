import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_lab_data():
    """Load wine quality data OR generate synthetic lab data"""
    try:
        # Try to load your winequality-red.csv first
        df = pd.read_csv('winequality-red.csv', sep=';')
        print("✅ Loaded winequality-red.csv (1599 samples)")
        # Rename columns to sound like lab measurements
        df = df.rename(columns={
            'fixed acidity': 'fixed_acidity',
            'volatile acidity': 'volatile_acidity', 
            'citric acid': 'citric_acid',
            'residual sugar': 'residual_sugar',
            'free sulfur dioxide': 'free_SO2',
            'total sulfur dioxide': 'total_SO2'
        })
        # Add fake timestamps
        df['timestamp'] = pd.date_range('2024-01-01', periods=len(df), freq='D')
        return df[['timestamp', 'pH', 'volatile_acidity', 'citric_acid', 
                  'residual_sugar', 'chlorides', 'free_SO2', 'total_SO2', 'alcohol']]
    except:
        # Fallback: generate synthetic data
        np.random.seed(42)
        n_samples = 200
        dates = pd.date_range('2024-01-01', periods=n_samples, freq='D')
        
        # Base means and std for each parameter (lab-like ranges)
        base_means = {'pH': 7.0, 'turbidity_NTU': 2.5, 'conductivity': 500}
        data = {}
        for param, mean in base_means.items():
            data[param] = np.random.normal(mean, 0.5, n_samples)
        
        # Add process shift and outliers
        data['pH'][100:120] += 1.2  # Process shift
        data['turbidity_NTU'][50] = 8.0  # Outlier
        
        df = pd.DataFrame(data)
        df['timestamp'] = dates
        print("⚠️  Generated synthetic data (wine file not found)")
        return df