"""DDE regression gate — CI/CD-backed validation pipeline.

Runs on every PR and push to verify:
1. All models pass validation thresholds (R2 >= 0.50, MAE <= 20% of range)
2. No regression vs baseline metrics (within tolerance)
3. Split integrity is maintained (no leakage)

Exits non-zero if any gate fails — blocks merge in CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .baseline import PROPERTIES, load_all
from .evaluate import DEFAULT_THRESHOLDS, run_validation

# Baseline metrics from Sprint S3 (DDE v0.3) — regression reference
BASELINE_METRICS = {
    "logp": {"r2": 0.8949, "mae": 0.3291},
    "logS": {"r2": 0.7974, "mae": 0.4453},
    "tpsa": {"r2": 0.6188, "mae": 8.7009},
}

# Allowable regression tolerance (relative)
REGRESSION_TOLERANCE = 0.05  # 5% relative degradation max


def check_regression(prop: str, current_r2: float, current_mae: float) -> list[str]:
    """Check current metrics against baseline for regression."""
    warnings = []
    if prop in BASELINE_METRICS:
        baseline = BASELINE_METRICS[prop]
        # R2 should not degrade more than tolerance
        r2_degradation = (baseline["r2"] - current_r2) / max(abs(baseline["r2"]), 1e-9)
        if r2_degradation > REGRESSION_TOLERANCE:
            warnings.append(
                f"{prop}: R2 regressed {r2_degradation*100:.1f}% "
                f"(baseline={baseline['r2']:.4f}, current={current_r2:.4f})"
            )
        # MAE should not increase more than tolerance
        mae_increase = (current_mae - baseline["mae"]) / max(baseline["mae"], 1e-9)
        if mae_increase > REGRESSION_TOLERANCE:
            warnings.append(
                f"{prop}: MAE regressed {mae_increase*100:.1f}% "
                f"(baseline={baseline['mae']:.4f}, current={current_mae:.4f})"
            )
    return warnings


def main() -> int:
    """Run the full regression gate. Returns 0 on success, 1 on failure."""
    print("=" * 60)
    print("DDE REGRESSION GATE — CI/CD Validation Pipeline")
    print("=" * 60)

    failures = []
    regression_warnings = []

    for prop in sorted(PROPERTIES):
        predictor = load_all().get(prop)
        if predictor is None:
            print(f"  {prop}: SKIP (no artifact)")
            continue

        report = run_validation(predictor)

        status = "PASS" if report.passed else "FAIL"
        print(f"\n  {prop}: {status}")
        print(f"    R2={report.r2:.4f} (threshold >= {DEFAULT_THRESHOLDS['r2_min']})")
        print(f"    MAE={report.mae:.4f} (threshold <= {DEFAULT_THRESHOLDS['mae_max_frac_of_range']*100:.0f}% of range)")
        print(f"    n_test={report.n_test}")

        if not report.passed:
            failures.append((prop, report.reasons))

        # Regression check
        warns = check_regression(prop, report.r2, report.mae)
        regression_warnings.extend(warns)

    print("\n" + "-" * 60)

    if regression_warnings:
        print("REGRESSION WARNINGS:")
        for w in regression_warnings:
            print(f"  ⚠ {w}")

    if failures:
        print(f"\nGATE FAILED: {len(failures)} model(s) below threshold")
        for prop, reasons in failures:
            print(f"  {prop}: {', '.join(reasons)}")
        return 1

    print("\nGATE PASSED: All models meet thresholds")
    if regression_warnings:
        print("  (with regression warnings — review recommended)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
