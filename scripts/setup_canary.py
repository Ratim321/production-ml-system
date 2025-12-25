"""Script to set up canary deployment"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import ModelVersion


def setup_canary(model_version: str, traffic_percent: int = 10):
    """Set up canary deployment for a model version"""
    db = SessionLocal()
    try:
        # Find the model version
        model = db.query(ModelVersion).filter(
            ModelVersion.version == model_version
        ).first()
        
        if not model:
            print(f"Model version {model_version} not found!")
            return False
        
        # Deprecate existing canary
        db.query(ModelVersion).filter(
            ModelVersion.status == "canary"
        ).update({"status": "deprecated"})
        
        # Set new canary
        model.status = "canary"
        model.traffic_percent = traffic_percent
        db.commit()
        
        print(f"Canary deployment set up for {model_version} with {traffic_percent}% traffic")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error setting up canary: {e}")
        return False
    finally:
        db.close()


def promote_canary(model_version: str):
    """Promote canary model to active"""
    db = SessionLocal()
    try:
        # Find the canary model
        canary = db.query(ModelVersion).filter(
            ModelVersion.version == model_version,
            ModelVersion.status == "canary"
        ).first()
        
        if not canary:
            print(f"Canary model {model_version} not found!")
            return False
        
        # Deprecate old active models
        db.query(ModelVersion).filter(
            ModelVersion.status == "active"
        ).update({"status": "deprecated"})
        
        # Promote canary to active
        canary.status = "active"
        canary.traffic_percent = 100
        
        # Deprecate other canaries
        db.query(ModelVersion).filter(
            ModelVersion.status == "canary",
            ModelVersion.version != model_version
        ).update({"status": "deprecated"})
        
        db.commit()
        
        print(f"Canary model {model_version} promoted to active")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error promoting canary: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage canary deployments")
    parser.add_argument("action", choices=["setup", "promote"], help="Action to perform")
    parser.add_argument("--version", required=True, help="Model version")
    parser.add_argument("--traffic", type=int, default=10, help="Traffic percentage for canary (default: 10)")
    
    args = parser.parse_args()
    
    if args.action == "setup":
        setup_canary(args.version, args.traffic)
    elif args.action == "promote":
        promote_canary(args.version)


