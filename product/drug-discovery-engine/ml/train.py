"""Train and persist all DDE model artifacts.

Usage:
    python -m ml.train
"""
from ml.baseline import PROPERTIES, train_and_persist

if __name__ == "__main__":
    for prop in PROPERTIES:
        p = train_and_persist(prop)
        print(f"trained and persisted {p.version} ({p.property_name}) -> ml/artifacts/")