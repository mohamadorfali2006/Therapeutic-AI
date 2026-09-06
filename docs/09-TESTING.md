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
- **10 pytest tests** pass (backend: health, predict valid/invalid, trace roundtrip, models list, validation gate, UI served, artifact present).
- **Regulated validation gate** PASS on locked test split: R2=0.6583, RMSE=0.8943, MAE=0.5293 (thresholds R2≥0.5, MAE≤20% of range) — `ml/evaluate.py`.
- **Playwright Visual QA (`tests/qa_dashboard.py`)**: 12/12 checks pass — title, health indicator, models table, predict flow renders value, theme toggle switches data-theme + canvas (`#0A0A0B` ↔ `#F7F6F3`), trace fetch button, invalid SMILES → 422.

_This document is living; expanded with concrete test suites as code lands._