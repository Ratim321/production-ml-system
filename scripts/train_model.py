"""Train ML model"""
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ml.trainer import ModelTrainer


def main():
    """Main training function"""
    # Load data
    data_path = Path("data/raw/customer_data.csv")
    if not data_path.exists():
        print("Data file not found. Generating synthetic data...")
        from scripts.generate_data import generate_customer_data
        df = generate_customer_data(n_samples=5000)
    else:
        df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} samples")
    print(f"Churn rate: {df['churn'].mean():.2%}")
    
    # Train model
    trainer = ModelTrainer()
    print("Training model...")
    run_id = trainer.train(df, model_type="random_forest")
    print(f"Model trained! MLflow run ID: {run_id}")
    print(f"View in MLflow UI: http://localhost:5000")


if __name__ == "__main__":
    main()


