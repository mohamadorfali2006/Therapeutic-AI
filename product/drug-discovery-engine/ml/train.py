"""Train and persist the DDE baseline model artifact.

Usage:
    python -m ml.train
"""
from ml.baseline import train_and_persist

if __name__ == "__main__":
    p = train_and_persist()
    print(f"trained and persisted {p.version} -> ml/artifacts/")