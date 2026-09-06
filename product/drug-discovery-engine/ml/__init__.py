"""ML package entry points and metadata."""

from .baseline import BaselinePredictor, load_default, train_and_persist
from .evaluate import (
    DEFAULT_THRESHOLDS,
    ValidationReport,
    run_validation,
)
from .features import feature_names, smiles_to_features
from .seed_data import DEMO_TARGETS, load_seed_data, target_range

__all__ = [
    "BaselinePredictor",
    "load_default",
    "train_and_persist",
    "run_validation",
    "ValidationReport",
    "DEFAULT_THRESHOLDS",
    "feature_names",
    "smiles_to_features",
    "DEMO_TARGETS",
    "load_seed_data",
    "target_range",
]

__version__ = "0.1.0"