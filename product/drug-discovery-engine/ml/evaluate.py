"""DDE evaluation + validation gate (Regulated-AI owned).

Implements the validation-gate contract described in
company/regulated-ai/02-sop.md:
- evaluate on the LOCKED test split (no leakage);
- compute RMSE, MAE, R2;
- produce a signed verdict dict with explicit pass/fail vs thresholds;
- log to provenance (handled by app layer).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from .baseline import SPLIT_SEED, BaselinePredictor, build_dataset

DEFAULT_THRESHOLDS = {
    "r2_min": 0.50,
    "mae_max_frac_of_range": 0.20,
}


@dataclass
class ValidationReport:
    model_version: str
    dataset_version: str
    n_test: int
    rmse: float
    mae: float
    r2: float
    target_min: float
    target_max: float
    thresholds: dict = field(default_factory=lambda: dict(DEFAULT_THRESHOLDS))
    passed: bool = False
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def _locked_test_split():
    X, y = build_dataset()
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SPLIT_SEED, shuffle=True
    )
    return X_test, y_test


def run_validation(predictor: BaselinePredictor,
                   thresholds: dict | None = None) -> ValidationReport:
    """Evaluate on the locked test split and produce a pass/fail verdict."""
    thr = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        thr.update(thresholds)

    X_test, y_test = _locked_test_split()
    pred = predictor.model.predict(X_test)

    rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
    mae = float(mean_absolute_error(y_test, pred))
    r2 = float(r2_score(y_test, pred))

    target_min = float(np.min(y_test))
    target_max = float(np.max(y_test))
    target_range = max(target_max - target_min, 1e-9)

    reasons: list[str] = []
    passed = True
    if r2 < thr["r2_min"]:
        passed = False
        reasons.append(
            f"R2 {r2:.3f} below threshold {thr['r2_min']}"
        )
    if mae > thr["mae_max_frac_of_range"] * target_range:
        passed = False
        reasons.append(
            f"MAE {mae:.3f} exceeds {thr['mae_max_frac_of_range']*100:.0f}% "
            f"of target range ({target_range:.2f})"
        )
    if not reasons:
        reasons.append("All thresholds met on locked test split.")

    return ValidationReport(
        model_version=predictor.version,
        dataset_version=predictor.dataset_version,
        n_test=int(len(y_test)),
        rmse=round(rmse, 4),
        mae=round(mae, 4),
        r2=round(r2, 4),
        target_min=round(target_min, 4),
        target_max=round(target_max, 4),
        thresholds=thr,
        passed=passed,
        reasons=reasons,
    )


if __name__ == "__main__":  # pragma: no cover
    from .baseline import load_default

    report = run_validation(load_default())
    print(report.to_json())
    print("PASS" if report.passed else "FAIL")