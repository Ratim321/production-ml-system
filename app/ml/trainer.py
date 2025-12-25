"""Model training with MLflow integration"""
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
from app.config import settings
from app.feature_store.transformer import FeatureTransformer
from app.database import SessionLocal
from app.models import ModelVersion, ModelMetrics
from datetime import datetime
import os


class ModelTrainer:
    """Train and register models with MLflow"""
    
    def __init__(self):
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(settings.mlflow_experiment_name)
        self.feature_transformer = FeatureTransformer()
    
    def train(self, df: pd.DataFrame, model_type: str = "random_forest") -> str:
        """Train a model and return MLflow run ID"""
        
        # Prepare data
        X = self.feature_transformer.transform_batch(df.drop('churn', axis=1))
        y = df['churn'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Fit feature transformer
        self.feature_transformer.fit(df.drop('churn', axis=1))
        
        # Train model
        with mlflow.start_run():
            if model_type == "random_forest":
                model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42
                )
            elif model_type == "gradient_boosting":
                model = GradientBoostingClassifier(
                    n_estimators=100,
                    max_depth=5,
                    random_state=42
                )
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", roc_auc)
            
            # Log parameters
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("n_samples", len(df))
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Save model locally
            run_id = mlflow.active_run().info.run_id
            os.makedirs(settings.model_registry_path, exist_ok=True)
            model_path = os.path.join(settings.model_registry_path, f"model_{run_id}.joblib")
            import joblib
            joblib.dump(model, model_path)
            
            # Register model version
            self._register_model_version(run_id, model_type, {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
                "roc_auc": float(roc_auc)
            })
            
            return run_id
    
    def _register_model_version(self, run_id: str, model_type: str, metrics: dict):
        """Register model version in database"""
        db = SessionLocal()
        try:
            version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            model_version = ModelVersion(
                version=version,
                model_type=model_type,
                status="active",
                traffic_percent=100,
                mlflow_run_id=run_id,
                performance_metrics=metrics
            )
            
            # Deprecate old active models
            db.query(ModelVersion).filter(
                ModelVersion.status == "active"
            ).update({"status": "deprecated"})
            
            db.add(model_version)
            db.commit()
            
            # Store metrics
            for metric_name, metric_value in metrics.items():
                metric_record = ModelMetrics(
                    model_version=version,
                    metric_name=metric_name,
                    metric_value=metric_value
                )
                db.add(metric_record)
            
            db.commit()
        finally:
            db.close()


