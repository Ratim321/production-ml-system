"""Generate synthetic customer churn data"""
import pandas as pd
import numpy as np
import random
from pathlib import Path


def generate_customer_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate synthetic customer churn dataset"""
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for i in range(n_samples):
        # Customer demographics
        age = np.random.randint(18, 80)
        gender = random.choice(['Male', 'Female'])
        partner = random.choice([True, False])
        dependents = random.choice([True, False]) if partner else False
        
        # Service details
        tenure = np.random.randint(0, 72)  # months
        phone_service = random.choice([True, False])
        multiple_lines = random.choice([True, False]) if phone_service else False
        
        internet_service = random.choice(['DSL', 'Fiber optic', 'No'])
        online_security = random.choice([True, False]) if internet_service != 'No' else False
        online_backup = random.choice([True, False]) if internet_service != 'No' else False
        device_protection = random.choice([True, False]) if internet_service != 'No' else False
        tech_support = random.choice([True, False]) if internet_service != 'No' else False
        streaming_tv = random.choice([True, False]) if internet_service != 'No' else False
        streaming_movies = random.choice([True, False]) if internet_service != 'No' else False
        
        # Contract and billing
        contract_type = random.choice(['Month-to-month', 'One year', 'Two year'])
        paperless_billing = random.choice([True, False])
        payment_method = random.choice([
            'Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'
        ])
        
        # Charges (correlated with services)
        base_monthly = 20 if internet_service == 'No' else 30
        if internet_service == 'Fiber optic':
            base_monthly += 20
        if multiple_lines:
            base_monthly += 10
        if streaming_tv or streaming_movies:
            base_monthly += 10
        
        monthly_charges = base_monthly + np.random.normal(0, 5)
        monthly_charges = max(20, min(120, monthly_charges))
        
        total_charges = monthly_charges * tenure + np.random.normal(0, 100)
        total_charges = max(0, total_charges)
        
        # Churn probability (higher for month-to-month, high charges, low tenure)
        churn_prob = 0.1
        if contract_type == 'Month-to-month':
            churn_prob += 0.3
        if tenure < 12:
            churn_prob += 0.2
        if monthly_charges > 70:
            churn_prob += 0.15
        if payment_method == 'Electronic check':
            churn_prob += 0.1
        if not online_security and internet_service != 'No':
            churn_prob += 0.05
        
        churn = np.random.random() < churn_prob
        
        data.append({
            'customer_id': f'CUST_{i+1:05d}',
            'age': age,
            'gender': gender,
            'partner': partner,
            'dependents': dependents,
            'tenure': tenure,
            'phone_service': phone_service,
            'multiple_lines': multiple_lines,
            'internet_service': internet_service,
            'online_security': online_security,
            'online_backup': online_backup,
            'device_protection': device_protection,
            'tech_support': tech_support,
            'streaming_tv': streaming_tv,
            'streaming_movies': streaming_movies,
            'contract_type': contract_type,
            'paperless_billing': paperless_billing,
            'payment_method': payment_method,
            'monthly_charges': round(monthly_charges, 2),
            'total_charges': round(total_charges, 2),
            'churn': int(churn)
        })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Generate training data
    print("Generating synthetic customer churn data...")
    df = generate_customer_data(n_samples=5000)
    
    # Save to CSV
    output_path = Path("data/raw/customer_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated {len(df)} samples")
    print(f"Churn rate: {df['churn'].mean():.2%}")
    print(f"Data saved to {output_path}")


