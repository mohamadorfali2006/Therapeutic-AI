# Company Sprint Report

- **Sprint:** S1 — Sprint 1: DDE v0.2
- **Goal:** Expand DDE: add 2nd property (logS solubility proxy) + richer fingerprints + property-routing in API
- **Status:** closed
- **Generated:** 2026-09-06T14:45:32+00:00

## Tasks

### T1 - logS solubility proxy: define approximate target set + domain justification (cdd)
- Status: done. Owner: Molecular Design Agent - (gate PASS)
Evidence:
- ml/logs_data.py parses; matches seed_data.py
- logS dataset accepted (57 records, range -4.8..-0.1)

### T2 - ECFP-style hashed fingerprints (pure Python) in ml/fingerprints.py (ai-research)
- Status: done. Owner: Predictive Modeling Scientist Agent - (gate PASS)
Evidence:
- ml/fingerprints.py + test_fingerprint_deterministic_and_size
- Fingerprints deterministic, ECFP-style, no RDKit

### T3 - Property-aware trainer: train property-specific artifacts (logp + logs) (ai-research)
- Status: done. Owner: Predictive Modeling Scientist Agent - (gate PASS)
Evidence:
- 15/15 pytest; ml/artifacts/baseline_{logp,logs}_v1.pkl
- Both models trained; features 17 counts + 256 fp

### T4 - Property routing in /api/v1/predict (property param + artifact selection) (platform-eng)
- Status: done. Owner: Platform Engineer Agent - (gate PASS)
Evidence:
- test_predict_unknown_property_503 + live /api/v1/predict
- Property routing live; unknown property 503

### T5 - Dataset versioning: seed-2026.09.06-v2 with logS; provenance (data)
- Status: done. Owner: Data Ops Agent - (gate PASS)
Evidence:
- company/data/05-logs-provenance.md
- Dataset v2 versioned and immutable

### T6 - Validation gate for logS model: metrics + thresholds report (regulated-ai)
- Status: done. Owner: Validation Scientist Agent - (gate PASS)
Evidence:
- company/regulated-ai/reports/2026-09-06-s1-gates.md
- BOTH gates PASS (logp R2=0.722, logS R2=0.608)

### T7 - Update v0.2 status + research-use disclaimer (regulatory)
- Status: done. Owner: Regulatory Affairs Agent - (gate PASS)
Evidence:
- company/regulatory/04-product-status.md
- v0.2 research-use status documented
