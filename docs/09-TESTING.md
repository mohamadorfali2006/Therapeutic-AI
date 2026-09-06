# 09-TESTING — Therapeutic-AI

## Testing philosophy
Because the product includes **FDA-cleared SaMD**, testing has two tracks:
1. **Engineering QA** — standard build/lint/test for the platform.
2. **Regulated ML validation** — formal V&V (IEC 62304), regression analysis, and PCCP-consistent retraining validation.

## Standard engineering track
| Layer | Tooling (planned) | Purpose |
|---|---|---|
| Unit | pytest / vitest | Component correctness |
| Integration | pytest + service-level | Internal/external interfaces |
| System / E2E | Playwright | Full flows (incl. clickability audit, Global2Design §4) |
| Lint | ruff (py), ESLint (js/ts) | Style + static |
| Security | SBOM, dependency scan, pen-test | FDA cybersecurity guidance |
| CI | GitHub Actions | Gate on every change |

**Verify commands (per global standard):** detect stack from markers; run `build`, `lint`, `test` after every change; never report passing if unrun/failing.

## Regulated ML validation track
| Area | Requirement | Evidence |
|---|---|---|
| Dataset integrity | Locked splits; no leakage | Versioned split registry, checksums |
| Model eval | Proper scoring, calibration, OOD, bias | Evaluation records on locked splits |
| Regression | Every change → regression analysis + regression testing | Regression test reports |
| V&V (IEC 62304) | Unit/integration/system with objective pass/fail | Test protocols + reports |
| PCCP | Each planned modification follows authorized Modification Protocol | PCCP evidence records |
| Post-market | Monitoring plan consistent with PCCP | Surveillance records |

## Checkpoints / gates
- Phase 2: validation-pipeline MVP (regression gates) live.
- Phase 3: evaluation/calibration framework operating.
- Phase 4: submission-ready V&V + post-market plan.

## Current status (DDE foundation)
- **15 pytest tests** pass (backend: health, logp + logS predict, unknown property 503, invalid SMILES 422, trace roundtrip both properties, models list, validate per-model + all, fingerprint determinism, UI served, artifacts present).
- **Regulated validation gates** PASS on locked test splits — `ml/evaluate.py`:
  - baseline-logp: R2=0.7222, RMSE=0.8063, MAE=0.4780 (dataset seed-2026.09.06)
  - baseline-logS: R2=0.6079, RMSE=0.8576, MAE=0.5242 (dataset seed-2026.09.06-v2)
  - Thresholds: R2>=0.5, MAE<=20% of range. Full report: `company/regulated-ai/reports/2026-09-06-s1-gates.md`.
- **Playwright Visual QA (`tests/qa_dashboard.py`)**: 14/14 checks pass — title, health, models table, predict (logp + logS via dropdown), theme toggle light canvas `#F7F6F3`, trace fetch, invalid SMILES 422.
- **Company runtime**: `python company/platform/run.py status` (S1 closed 7/7, all gates PASS).

_This document is living; expanded with concrete test suites as code lands._