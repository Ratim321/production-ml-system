"""Unit tests for feature store"""
import pytest
import pandas as pd
from app.feature_store.transformer import FeatureTransformer


def test_feature_transformer_fit_transform():
    """Test feature transformer fit and transform"""
    transformer = FeatureTransformer()
    
    # Create sample data
    df = pd.DataFrame({
        'age': [25, 35, 45],
        'tenure': [12, 24, 36],
        'monthly_charges': [50.0, 70.0, 90.0],
        'total_charges': [600.0, 1680.0, 3240.0],
        'contract_type': ['Month-to-month', 'One year', 'Two year'],
        'payment_method': ['Electronic check', 'Bank transfer', 'Credit card'],
        'internet_service': ['DSL', 'Fiber optic', 'No'],
        'paperless_billing': [True, False, True],
        'gender': ['Male', 'Female', 'Male'],
        'partner': [False, True, False],
        'dependents': [False, True, False],
        'phone_service': [True, True, False],
        'multiple_lines': [False, True, False],
        'online_security': [False, True, False],
        'online_backup': [False, True, False],
        'device_protection': [False, True, False],
        'tech_support': [False, True, False],
        'streaming_tv': [True, False, True],
        'streaming_movies': [True, False, True]
    })
    
    # Fit transformer
    transformer.fit(df)
    
    # Transform
    features = transformer.transform_batch(df)
    
    assert features.shape[0] == 3
    assert features.shape[1] == 19  # Number of features


def test_feature_transformer_single_transform():
    """Test single customer transformation"""
    transformer = FeatureTransformer()
    
    df = pd.DataFrame({
        'age': [25],
        'tenure': [12],
        'monthly_charges': [50.0],
        'total_charges': [600.0],
        'contract_type': ['Month-to-month'],
        'payment_method': ['Electronic check'],
        'internet_service': ['DSL'],
        'paperless_billing': [True],
        'gender': ['Male'],
        'partner': [False],
        'dependents': [False],
        'phone_service': [True],
        'multiple_lines': [False],
        'online_security': [False],
        'online_backup': [False],
        'device_protection': [False],
        'tech_support': [False],
        'streaming_tv': [True],
        'streaming_movies': [True]
    })
    
    transformer.fit(df)
    
    customer_data = df.iloc[0].to_dict()
    features = transformer.transform(customer_data)
    
    assert features.shape[0] == 1
    assert features.shape[1] == 19


