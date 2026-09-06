"""ML package entry points and metadata."""

from .baseline import (
    BaselinePredictor,
    FEATURE_NAMES,
    available_properties,
    load_all,
    load_default,
    train_and_persist,
)
from .evaluate import (
    DEFAULT_THRESHOLDS,
    ValidationReport,
    run_validation,
)
from .features import feature_names, smiles_to_features
from .fingerprints import fingerprint_feature_names, smiles_to_fingerprint
from .seed_data import DEMO_TARGETS, load_seed_data, target_range

__all__ = [
    "BaselinePredictor",
    "load_default",
    "load_all",
    "train_and_persist",
    "run_validation",
    "ValidationReport",
    "DEFAULT_THRESHOLDS",
    "feature_names",
    "smiles_to_features",
    "available_properties",
    "fingerprint_feature_names",
    "smiles_to_fingerprint",
    "FEATURE_NAMES",
    "DEMO_TARGETS",
    "load_seed_data",
    "target_range",
]

__version__ = "0.2.0"