"""DDE property predictor (RandomForest regressor on molecular features).

Owned by company/ai-research. Deterministic: fixed random state and locked
dataset splits. Persists one artifact per demo property under ml/artifacts/.

Feature space: molecular count descriptors (ml/features) concatenated with
ECFP-style hashed fingerprints (ml/fingerprints) — feature count MUST match the
FEATURE_NAMES here; a mismatch aborts training (safety for model drift).
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

from .features import DEFAULT_FEATURE_NAMES, smiles_to_features
from .fingerprints import fingerprint_feature_names, smiles_to_fingerprint
from . import seed_data

ARTIFACT_DIR = Path(__file__).parent / "artifacts"

PROPERTIES = {
    "logp": {
        "module": seed_data,
        "dataset_version": "seed-2026.09.06",
        "artifact": ARTIFACT_DIR / "baseline_logp_v1.pkl",
    },
    "logS": {
        "loader": "logs",
        "dataset_version": "seed-2026.09.06-v2",
        "artifact": ARTIFACT_DIR / "baseline_logs_v1.pkl",
    },
}

SPLIT_SEED = 42
MODEL_VERSION = "baseline-v1.0.0"

FEATURE_NAMES = list(DEFAULT_FEATURE_NAMES) + fingerprint_feature_names()

DEFAULT_ARTIFACT = PROPERTIES["logp"]["artifact"]


def available_properties() -> list[str]:
    return sorted(PROPERTIES)


def property_meta(prop: str) -> dict:
    if prop not in PROPERTIES:
        raise KeyError(f"Unknown property: {prop!r}. Known: {sorted(PROPERTIES)}")
    info = PROPERTIES[prop]
    return {
        "property": prop,
        "model_version": MODEL_VERSION,
        "dataset_version": info["dataset_version"],
        "artifact": str(info["artifact"]),
    }


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
        vec = smiles_to_extended_features(smiles)
        if len(vec) != len(self.features):
            raise ValueError("Feature vector length mismatch.")
        arr = np.asarray([vec], dtype=np.float64)
        value = float(self.model.predict(arr)[0])
        return value

    def confidence(self) -> float:
        return 1.0  # demo confidence placeholder

    def save(self, path: Path | None = None) -> None:
        path = Path(path) if path else Path(self.artifact_path())
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    def artifact_path(self) -> str:
        return PROPERTIES[self.property_name]["artifact"]

    def to_meta(self) -> dict:
        return {
            "model_version": self.version,
            "dataset_version": self.dataset_version,
            "property": self.property_name,
            "features": self.features,
            "n_features": len(self.features),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }


def _load_dataset_loader(prop: str):
    if prop == "logp":
        return seed_data.load_seed_data
    from . import logs_data
    return logs_data.load_seed_data


def smiles_to_extended_features(smiles: str) -> list[float]:
    """Count descriptors + ECFP-style fingerprint."""
    return list(smiles_to_features(smiles)) + list(smiles_to_fingerprint(smiles))


def build_dataset(prop: str = "logp"):
    """Return X (feature matrix), y (targets). Raises if SMILES unparseable."""
    if prop not in PROPERTIES:
        raise KeyError(prop)
    loader = _load_dataset_loader(prop)
    X: list[list[float]] = []
    y: list[float] = []
    for smiles, target in loader():
        X.append(smiles_to_extended_features(smiles))
        y.append(float(target))
    return np.asarray(X, dtype=np.float64), np.asarray(y, dtype=np.float64)


def train_and_persist(prop: str = "logp",
                      path: Path | None = None,
                      metadata_path: Path | None = None) -> BaselinePredictor:
    if prop not in PROPERTIES:
        raise KeyError(prop)
    info = PROPERTIES[prop]
    X, y = build_dataset(prop)
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
        dataset_version=info["dataset_version"],
        property_name=prop,
        features=list(FEATURE_NAMES),
    )
    save_path = Path(path) if path else info["artifact"]
    predictor.save(save_path)

    meta = predictor.to_meta()
    meta.update({
        "n_records": int(len(X)),
        "test_size": 0.2,
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),
        "split_seed": SPLIT_SEED,
        "split_lock": "deterministic:train_test_split(seed=42)",
    })
    meta_path = Path(metadata_path) if metadata_path else save_path.with_name(save_path.stem + "_meta.json")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    return predictor


def load_default(prop: str = "logp", path: Path | None = None) -> BaselinePredictor:
    if prop not in PROPERTIES:
        raise KeyError(prop)
    p = Path(path) if path else PROPERTIES[prop]["artifact"]
    if not p.exists():
        raise FileNotFoundError(
            f"No model artifact at {p}. Run `python -m ml.train` first."
        )
    with open(p, "rb") as fh:
        return pickle.load(fh)


def load_all() -> dict[str, BaselinePredictor]:
    predictors = {}
    for prop in PROPERTIES:
        try:
            predictors[prop] = load_default(prop)
        except FileNotFoundError:
            continue
    return predictors


def available_models_dir() -> list[Path]:
    return sorted(ARTIFACT_DIR.glob("*.pkl"))


if __name__ == "__main__":  # pragma: no cover
    for prop in PROPERTIES:
        p = train_and_persist(prop)
        print(json.dumps(p.to_meta(), indent=2))