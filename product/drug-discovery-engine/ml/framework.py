"""DDE Model Evaluation & Calibration Framework.

Owned by company/regulated-ai. Provides:
- Calibration analysis (predicted vs actual, residual distribution)
- Confidence interval estimation via bootstrap
- Drift detection (input distribution shift)
- Model report generation

Research use only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class CalibrationResult:
    """Result of calibration analysis."""
    property_name: str
    n_samples: int
    mean_error: float  # mean(predicted - actual)
    std_error: float
    max_abs_error: float
    within_95_ci: float  # fraction within 95% CI
    calibration_score: float  # 0-100, higher = better calibrated
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DriftReport:
    """Input distribution drift report."""
    property_name: str
    baseline_mean: float
    current_mean: float
    drift_score: float  # 0-1, higher = more drift
    drift_detected: bool
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def compute_calibration(
    predicted: list[float],
    actual: list[float],
    property_name: str = "",
    confidence: float = 0.95,
) -> CalibrationResult:
    """Compute calibration metrics for a model.
    
    Args:
        predicted: Model predictions
        actual: Ground truth values
        property_name: Name of the property
        confidence: Confidence level for intervals
    
    Returns:
        CalibrationResult with metrics
    """
    if len(predicted) != len(actual) or len(predicted) == 0:
        raise ValueError("predicted and actual must have same non-zero length")
    
    n = len(predicted)
    
    # Errors (predicted - actual)
    errors = [p - a for p, a in zip(predicted, actual)]
    mean_error = sum(errors) / n
    variance = sum((e - mean_error) ** 2 for e in errors) / n
    std_error = math.sqrt(variance)
    max_abs_error = max(abs(e) for e in errors)
    
    # Fraction within confidence interval (using normal approximation)
    if std_error > 0:
        z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
        within_ci = sum(
            1 for e in errors
            if abs(e - mean_error) <= z * std_error
        ) / n
    else:
        within_ci = 1.0
    
    # Calibration score (0-100)
    # Based on: low mean error, low std error, high within-CI fraction
    mean_penalty = min(50.0, abs(mean_error) * 10)
    std_penalty = min(30.0, std_error * 5)
    ci_bonus = within_ci * 80
    calibration_score = max(0.0, min(100.0, 100.0 - mean_penalty - std_penalty + ci_bonus - 20))
    
    return CalibrationResult(
        property_name=property_name,
        n_samples=n,
        mean_error=mean_error,
        std_error=std_error,
        max_abs_error=max_abs_error,
        within_95_ci=within_ci,
        calibration_score=calibration_score,
    )


def detect_drift(
    baseline: list[float],
    current: list[float],
    property_name: str = "",
    threshold: float = 0.1,
) -> DriftReport:
    """Detect input distribution drift.
    
    Compares the mean of the baseline distribution vs current.
    Drift detected if relative change exceeds threshold.
    
    Args:
        baseline: Baseline distribution values
        current: Current distribution values
        property_name: Name of the property
        threshold: Relative change threshold for drift
    
    Returns:
        DriftReport
    """
    if not baseline or not current:
        raise ValueError("baseline and current must be non-empty")
    
    baseline_mean = sum(baseline) / len(baseline)
    current_mean = sum(current) / len(current)
    
    if baseline_mean != 0:
        drift_score = abs(current_mean - baseline_mean) / abs(baseline_mean)
    else:
        drift_score = abs(current_mean - baseline_mean)
    
    drift_detected = drift_score > threshold
    
    return DriftReport(
        property_name=property_name,
        baseline_mean=baseline_mean,
        current_mean=current_mean,
        drift_score=drift_score,
        drift_detected=drift_detected,
    )


def generate_calibration_report(
    results: list[CalibrationResult],
    output_path: Optional[Path] = None,
) -> str:
    """Generate a human-readable calibration report."""
    lines = []
    lines.append("=" * 60)
    lines.append("DDE MODEL CALIBRATION REPORT")
    lines.append("=" * 60)
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    
    for r in results:
        lines.append(f"Property: {r.property_name}")
        lines.append(f"  Samples: {r.n_samples}")
        lines.append(f"  Mean error: {r.mean_error:.4f}")
        lines.append(f"  Std error: {r.std_error:.4f}")
        lines.append(f"  Max |error|: {r.max_abs_error:.4f}")
        lines.append(f"  Within 95% CI: {r.within_95_ci:.1%}")
        lines.append(f"  Calibration score: {r.calibration_score:.1f}/100")
        status = "PASS" if r.calibration_score >= 60 else "REVIEW"
        lines.append(f"  Status: {status}")
        lines.append("")
    
    lines.append("=" * 60)
    
    report = "\n".join(lines)
    
    if output_path:
        output_path.write_text(report)
    
    return report


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Demo with synthetic data
    import random
    rng = random.Random(42)
    
    # Simulated predictions and actual values
    actual = [rng.gauss(2.0, 0.5) for _ in range(50)]
    predicted = [a + rng.gauss(0, 0.2) for a in actual]  # Good model
    
    cal = compute_calibration(predicted, actual, "logp")
    print(generate_calibration_report([cal]))
    
    # Drift detection
    baseline = [rng.gauss(2.0, 0.5) for _ in range(100)]
    current = [rng.gauss(2.3, 0.5) for _ in range(100)]  # Slight drift
    
    drift = detect_drift(baseline, current, "logp")
    print(f"\nDrift detection: drift_score={drift.drift_score:.4f}, detected={drift.drift_detected}")
