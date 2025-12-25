"""Batch inference script"""
import sys
import pandas as pd
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.prediction_service import PredictionService
from app.schemas import CustomerFeatures


def main():
    """Run batch inference"""
    # Load data
    data_path = Path("data/raw/customer_data.csv")
    if not data_path.exists():
        print("Data file not found!")
        return
    
    df = pd.read_csv(data_path)
    
    # Convert to CustomerFeatures
    customers = []
    for _, row in df.iterrows():
        customer = CustomerFeatures(
            customer_id=row['customer_id'],
            age=int(row['age']),
            tenure=int(row['tenure']),
            monthly_charges=float(row['monthly_charges']),
            total_charges=float(row['total_charges']),
            contract_type=row['contract_type'],
            payment_method=row['payment_method'],
            paperless_billing=bool(row['paperless_billing']),
            gender=row['gender'],
            partner=bool(row['partner']),
            dependents=bool(row['dependents']),
            phone_service=bool(row['phone_service']),
            multiple_lines=bool(row['multiple_lines']),
            internet_service=row['internet_service'],
            online_security=bool(row['online_security']),
            online_backup=bool(row['online_backup']),
            device_protection=bool(row['device_protection']),
            tech_support=bool(row['tech_support']),
            streaming_tv=bool(row['streaming_tv']),
            streaming_movies=bool(row['streaming_movies'])
        )
        customers.append(customer)
    
    # Run batch prediction
    print(f"Running batch inference on {len(customers)} customers...")
    service = PredictionService()
    predictions = service.predict_batch(customers)
    
    # Save results
    results = pd.DataFrame([
        {
            'customer_id': p.customer_id,
            'prediction': p.prediction,
            'probability': p.probability,
            'model_version': p.model_version
        }
        for p in predictions
    ])
    
    output_path = Path("data/predictions/batch_predictions.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)
    
    print(f"Batch inference complete! Results saved to {output_path}")
    print(f"Average churn probability: {results['probability'].mean():.2%}")


if __name__ == "__main__":
    main()


