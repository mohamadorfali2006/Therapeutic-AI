"""DDE baseline property predictor (RandomForest regressor on molecular features).

Owned by company/ai-research. Deterministic: fixed random state and locked
dataset splits. Persists artifacts under ml/artifacts/.
"""

from __future__ import annotations

import json
import os
import pickle
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from .features import smiles_to_features
from .seed_data import load_seed_data

ARTIFACT_DIR = Path(__file__).parent / "artifacts"
DEFAULT_ARTIFACT = ARTIFACT_DIR / "baseline_v1.pkl"
METADATA_FILE = ARTIFACT_DIR / "baseline_v1_meta.json"
SPLIT_SEED = 42
MODEL_VERSION = "baseline-v1.0.0"
DATASET_VERSION = "seed-2026.09.06"
PROPERTY = "logp"
FEATURE_NAMES = [
    "heavy_atoms", "carbon", "nitrogen", "oxygen", "sulfur", "phosphorus",
    "halogen", "aromatic_atoms", "aliphatic_atoms", "single_bonds",
    "double_bonds", "triple_bonds", "aromatic_bonds", "branches",
    "rings_approx", "charge", "mw_proxy",
]


class BaselinePredictor:
    """Small regressor wrapping a fitted sklearn RandomForest."""

    def __init__(self, model, version: str, dataset_version: str,
                 property_name: str, features: list[str]):
        self.model = model
        self.version = version
        self.dataset_version = dataset_version
        self.property_name = property_name
        self.features = features

    def predict(self, smiles: str) -> float:
        vec = smiles_to_features(smiles)
        if len(vec) != len(self.features):
            raise ValueError("Feature vector length mismatch.")
        arr = np.asarray([vec], dtype=np.float64)
        value = float(self.model.predict(arr)[0])
        return value

    def confidence(self) -> float:
        return 1.0  # demo confidence placeholder

    def save(self, path: Path = DEFAULT_ARTIFACT) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    def to_meta(self) -> dict:
        return {
            "model_version": self.version,
            "dataset_version": self.dataset_version,
            "property": self.property_name,
            "features": self.features,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }


def build_dataset():
    """Return X (feature matrix), y (targets). Raises if SMILES unparseable."""
    data = load_seed_data()
    X: list[list[float]] = []
    y: list[float] = []
    for smiles, target in data:
        X.append(smiles_to_features(smiles))
        y.append(float(target))
    return np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)


def train_and_persist(path: Path = DEFAULT_ARTIFACT,
                      metadata_path: Path = METADATA_FILE) -> BaselinePredictor:
    X, y = build_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SPLIT_SEED, shuffle=True
    )
    rf = RandomForestRegressor(
        n_estimators=200, max_depth=None, random_state=SPLIT_SEED, n_jobs=1
    )
    rf.fit(X_train, y_train)

    predictor = BaselinePredictor(
        model=rf,
        version=MODEL_VERSION,
        dataset_version=DATASET_VERSION,
        property_name=PROPERTY,
        features=list(FEATURE_NAMES),
    )
    predictor.save(path)
    meta = predictor.to_meta()
    meta.update({
        "n_records": int(len(X)),
        "test_size": 0.2,
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),
        "split_seed": SPLIT_SEED,
        "split_lock": "deterministic:train_test_split(seed=42)",
    })
    metadata_path = Path(metadata_path)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metadata_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    return predictor


def load_default(path: Path = DEFAULT_ARTIFACT) -> BaselinePredictor:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"No model artifact at {path}. Run `python -m ml.train` first."
        )
    with open(path, "rb") as fh:
        return pickle.load(fh)


def available_models_dir() -> list[Path]:
    return sorted(ARTIFACT_DIR.glob("*.pkl"))


if __name__ == "__main__":  # pragma: no cover
    p = train_and_persist()
    print(json.dumps(p.to_meta(), indent=2))