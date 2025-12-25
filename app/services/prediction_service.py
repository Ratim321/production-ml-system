"""Prediction service for handling inference requests"""
import random
from typing import List, Dict, Any
from datetime import datetime
from app.ml.model_manager import ModelManager
from app.schemas import CustomerFeatures, PredictionResponse
from app.database import SessionLocal
from app.models import Prediction
from app.config import settings


class PredictionService:
    """Service for making predictions"""
    
    def __init__(self):
        self.model_manager = ModelManager()
    
    def predict_single(self, customer: CustomerFeatures) -> PredictionResponse:
        """Make single prediction"""
        # Transform features
        customer_dict = customer.dict()
        features = self.model_manager.feature_transformer.transform(customer_dict)
        
        # Determine if should use canary
        use_canary = (
            self.model_manager.canary_model is not None and
            random.randint(1, 100) <= settings.canary_traffic_percent
        )
        
        # Make prediction
        prediction, probability = self.model_manager.predict(features, use_canary)
        
        model_version = (
            self.model_manager.canary_version if use_canary
            else self.model_manager.model_version
        )
        
        # Store prediction
        self._store_prediction(customer.customer_id, prediction, probability, model_version, customer_dict)
        
        return PredictionResponse(
            customer_id=customer.customer_id,
            prediction=prediction,
            probability=probability,
            model_version=model_version,
            timestamp=datetime.now()
        )
    
    def predict_batch(self, customers: List[CustomerFeatures]) -> List[PredictionResponse]:
        """Make batch predictions"""
        import pandas as pd
        
        # Convert to DataFrame
        customer_dicts = [c.dict() for c in customers]
        df = pd.DataFrame(customer_dicts)
        
        # Transform features
        features = self.model_manager.feature_transformer.transform_batch(df)
        
        # Make predictions
        model = self.model_manager.current_model
        if model is None:
            raise ValueError("No model loaded")
        
        predictions = model.predict(features)
        probabilities = model.predict_proba(features)[:, 1]
        
        # Create responses
        responses = []
        model_version = self.model_manager.model_version
        
        for i, customer in enumerate(customers):
            response = PredictionResponse(
                customer_id=customer.customer_id,
                prediction=float(predictions[i]),
                probability=float(probabilities[i]),
                model_version=model_version,
                timestamp=datetime.now()
            )
            responses.append(response)
            
            # Store prediction
            self._store_prediction(
                customer.customer_id,
                float(predictions[i]),
                float(probabilities[i]),
                model_version,
                customer_dicts[i]
            )
        
        return responses
    
    def _store_prediction(self, customer_id: str, prediction: float, probability: float,
                         model_version: str, features: Dict[str, Any]):
        """Store prediction in database"""
        db = SessionLocal()
        try:
            pred_record = Prediction(
                customer_id=customer_id,
                prediction=prediction,
                probability=probability,
                model_version=model_version,
                features=features
            )
            db.add(pred_record)
            db.commit()
        finally:
            db.close()


