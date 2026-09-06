# Regulated AI / ML-Validation — Validation Gate SOP

> Standard Operating Procedure for validating a candidate model artifact before it enters
> the DDE staging or production environment. Every agent in this department follows this
> procedure without exception.

**SOP ID:** SOP-REG-001
**Version:** 1.0
**Effective:** 2026-09-06
**Owner:** Director, ML Validation Agent

---

## 1. Purpose

Define the step-by-step procedure for receiving, verifying, and rendering a validation verdict on a candidate model artifact submitted by AI Research. The output of this SOP is a signed, auditable validation verdict that the DDE's `/api/v1/validate` endpoint and provenance system consume.

## 2. Preconditions

Before this SOP begins:
- AI Research has submitted a candidate model artifact (trained weights + metadata) and an evaluation report matching the schema in `01-agents.md` §5.
- The evaluation report includes `model_id`, `model_version`, `training_run_id`, `dataset_version`, `split_checksum`, and the full `metrics` block.
- The `ml/evaluate.py` script and `/api/v1/validate` endpoint are operational and passing their own tests.

## 3. Procedure

### Step 1: Receive and Queue

| Action | Detail |
|---|---|
| Trigger | AI Research POSTs evaluation report to `/api/v1/validate` or commits it to provenance |
| Assignee | V&V Test Engineer Agent (regulated-ai-02) |
| Validation | Confirm evaluation report schema matches `evaluation-schema.json` (all required fields present, correct types) |
| On schema fail | Return `422` with field-level errors. Do not proceed. |
| Log | Write reception entry to `qms/audit-log.jsonl` with timestamp, model_id, and received_by |

### Step 2: Verify Locked Test Split Integrity

| Action | Detail |
|---|---|
| Assignee | Data Governance Engineer Agent (regulated-ai-03) |
| Check A | Compare `split_checksum` in the evaluation report against the checksum stored in `data/split-registry.json` for the declared `dataset_version` |
| Check B | Confirm the test split file hash (SHA-256) matches the registry entry at evaluation time |
| Check C | Verify no training data appears in the test split (leakage scan via ID overlap and feature-vector comparison) |
| **If Check A or B fails** | **AUTOMATIC FAIL** — quarantine the candidate model artifact immediately. Write quarantine record to `provenance/quarantine-log.json`. Route to QMS Agent for CAPA. |
| **If Check C detects leakage** | **AUTOMATIC FAIL** — quarantine model artifact + test split. Write quarantine record. Route to QMS Agent for CAPA. |
| Output | `reports/split-integrity-{run_id}.json` with `pass: true/false` and `checks: [A, B, C]` |

### Step 3: Check Metrics Against Thresholds

| Action | Detail |
|---|---|
| Assignee | V&V Test Engineer Agent (regulated-ai-02) |
| Source | `metrics` block from the evaluation report |

**Default thresholds (regression tasks):**

| Metric | Threshold | Logic |
|---|---|---|
| R-squared (R2) | >= 0.5 | Model explains at least 50% of variance |
| Mean Absolute Error (MAE) | <= 20% of target range | Error stays within acceptable tolerance |
| Monotonic sanity | TRUE | For properties where monotonic behavior is expected (e.g., logP), predicted-vs-actual must not violate monotonicity |

**Default thresholds (classification tasks):**

| Metric | Threshold | Logic |
|---|---|---|
| Calibration error | <= 0.10 | Predicted probabilities align with observed frequencies |
| R-squared (R2) | >= 0.5 | Baseline regression sanity check if applicable |
| Monotonic sanity | TRUE | Where applicable |

**Pass/fail logic:**

```
METRICS_PASS = (R2 >= 0.5) AND (MAE <= 0.20 * target_range) AND (monotonic_sanity == TRUE)
CLASSIFICATION_PASS = (calibration_error <= 0.10) AND (R2 >= 0.5) AND (monotonic_sanity == TRUE)
```

If the task type is ambiguous, apply regression thresholds by default. The V&V Test Engineer documents which thresholds were applied in the test report.

| On threshold fail | Record exact failure reason(s). Do NOT quarantine (data is fine, model is below bar). Return FAIL verdict with reasons. |
| Output | `reports/vv-test-report-{run_id}.json` with `metrics_evaluation: pass/fail` and per-metric results |

### Step 4: Verify PCCP Authorization (If Retraining)

| Action | Detail |
|---|---|
| Assignee | QMS / Change-Control Agent (regulated-ai-04) |
| Condition | Only if this candidate is a retraining (not a first-time model) |
| Check A | Confirm a pre-authorized Modification Protocol exists for this training recipe in `provenance/pccp-protocols/` |
| Check B | Verify the training run stayed within the authorized bounds (architecture, data source, hyperparameter ranges) |
| **If no protocol exists** | **FAIL** — retraining without PCCP authorization is not permitted. |
| **If bounds were violated** | **FAIL** — deviation from authorized protocol requires a new full validation from scratch. |
| Output | Entry in `qms/audit-log.jsonl` linking training_run_id to protocol_id |

### Step 5: Produce Signed Validation Verdict

| Action | Detail |
|---|---|
| Assignee | Director, ML Validation Agent (regulated-ai-01) |
| Input | Results from Steps 2, 3, and 4 |
| Decision | If ALL steps passed: verdict = PASS. If ANY step failed: verdict = FAIL. |

**Verdict record (JSON):**

```json
{
  "validation_id": "uuid — generated at verdict time",
  "model_id": "from evaluation report",
  "model_version": "from evaluation report",
  "verdict": "PASS | FAIL",
  "checks": {
    "split_integrity": "PASS | FAIL",
    "metrics_thresholds": "PASS | FAIL",
    "pccp_authorization": "PASS | FAIL | N/A"
  },
  "failure_reasons": ["only populated if FAIL"],
  "thresholds_applied": { "r2_min": 0.5, "mae_max_pct": 20.0, ... },
  "signed_by": "regulated-ai-01",
  "signed_at": "ISO-8601 timestamp"
}
```

| On PASS | Model artifact is marked eligible-for-deployment. Verdict written to `provenance/validation-verdicts.json`. |
| On FAIL | Model artifact is rejected. Verdict written to provenance with failure reasons. Routed back to AI Research with actionable details. |

### Step 6: Log to Provenance

| Action | Detail |
|---|---|
| Assignee | QMS / Change-Control Agent (regulated-ai-04) |
| Write | Append verdict to `provenance/validation-verdicts.json` |
| Write | Append entry to `qms/audit-log.jsonl` with full trail: reception, each check result, verdict, timestamp |
| Write | If PASS: update model status in model registry to `validated` |
| Write | If FAIL: update model status to `rejected` |

### Step 7: Release Gate

| Action | Detail |
|---|---|
| Assignee | QMS / Change-Control Agent (regulated-ai-04) |
| Condition | Only on PASS verdict |
| Action | Issue release authorization record (`qms/release-auth-{id}.json`) linking to validation_id |
| Effect | `/api/v1/validate` now allows production predictions for this model_version |
| Without this step | The API will not serve predictions even if the model file is physically present |

---

## 4. Escalation

| Situation | Escalation path |
|---|---|
| Schema ambiguity or novel metric | V&V Test Engineer raises to Director |
| Split integrity dispute with Data dept | Data Governance Engineer raises to Director |
| PCCP protocol not yet drafted | QMS Agent raises to Director + Regulatory dept |
| Director override request | Director raises to CRQO; override requires written CRQO approval + QMS CCR |
| Two consecutive FAILs on same model_id | Automatic CAPA trigger via QMS Agent |

## 5. Records Retention

All validation records (verdicts, test reports, split integrity reports, audit logs) are retained for the lifetime of the DDE product plus 2 years per FDA 21 CFR Part 11 requirements. Records are stored in `provenance/` and `qms/` directories with SHA-256 integrity hashes.

---

_SOP-REG-001 v1.0 — Regulated AI / ML-Validation department._
