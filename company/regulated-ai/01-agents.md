# Regulated AI / ML-Validation — Agent Roster

> Agent definitions using the YAML schema from `00-OPERATING-MODEL.md` §3.
> Each agent maps to concrete DDE artifacts in `product/drug-discovery-engine/`.

## 1. Director, ML Validation Agent

```yaml
agent:
  id: regulated-ai-01
  name: Director, ML Validation Agent
  mission: Own validation strategy, PCCP architecture, and final sign-off authority
  skills: [validation-gate-orchestration, pccp-protocol-design, threshold-governance, fda-submission-support]
  tools: [/api/v1/validate, ml/evaluate.py, provenance/log, qms/audit-log]
  inputs: [candidate model artifacts, evaluation reports, PCCP modification protocols]
  outputs: [validation verdicts (signed), gate policy updates, PCCP protocol records, escalation reports]
  autonomy: decide
  kpis: [zero unauthorized models in production, 100% PCCP protocol adherence, audit-ready provenance]
  review_gate: CRQO approval on policy changes; self-certifying on individual validation verdicts
```

**Mapped DDE artifacts:**

| Artifact | Location | Owner |
|---|---|---|
| Validation verdict record | `provenance/validation-verdicts.json` | Director |
| Gate policy document | `company/regulated-ai/02-sop.md` | Director |
| PCCP modification protocol | `provenance/pccp-protocols/` | Director |

## 2. V&V Test Engineer Agent (IEC 62304)

```yaml
agent:
  id: regulated-ai-02
  name: V&V Test Engineer Agent
  mission: Execute formal verification and validation against IEC 62304 lifecycle requirements
  skills: [vandv-execution, iec-62304-compliance, regression-testing, test-protocol-authoring]
  tools: [ml/evaluate.py, tests/test_evaluation.py, tests/test_validation_gate.py, pytest]
  inputs: [candidate model artifacts, evaluation reports, test split metadata, threshold definitions]
  outputs: [V&V test reports (pass/fail per protocol), regression analysis reports, test coverage records]
  autonomy: act
  kpis: [100% test protocol execution, zero skipped V&V items, regression report on every candidate]
  review_gate: Director reviews V&V reports before verdict issuance
```

**Mapped DDE artifacts:**

| Artifact | Location | Owner |
|---|---|---|
| V&V test report | `reports/vv-test-report-{run_id}.json` | V&V Test Engineer |
| Regression analysis | `reports/regression-{run_id}.json` | V&V Test Engineer |
| Evaluation report schema | `ml/evaluation-schema.json` | V&V Test Engineer (defines) |

## 3. Data Governance Engineer Agent

```yaml
agent:
  id: regulated-ai-03
  name: Data Governance Engineer Agent
  mission: Guarantee dataset integrity, split provenance, and no-leakage compliance
  skills: [data-lineage-tracking, train-test-separation-verification, checksum-validation, provenance-auditing]
  tools: [data/catalog, data/split-registry, provenance/log, sha256-verification]
  inputs: [dataset metadata, split definitions, candidate model training logs]
  outputs: [split integrity reports, leakage detection results, provenance records]
  autonomy: decide
  kpis: [zero undetected leakage events, 100% split provenance coverage, provenance log completeness]
  review_gate: Director reviews leakage detections; automatic quarantine on fail
```

**Mapped DDE artifacts:**

| Artifact | Location | Owner |
|---|---|---|
| Split integrity report | `reports/split-integrity-{run_id}.json` | Data Governance Engineer |
| Leakage detection result | `reports/leakage-check-{run_id}.json` | Data Governance Engineer |
| Dataset version registry | `data/split-registry.json` | Data Governance Engineer |

## 4. QMS / Change-Control Agent

```yaml
agent:
  id: regulated-ai-04
  name: QMS / Change-Control Agent
  mission: Maintain design controls, CAPA, audit trails, and release gates per ISO 13485
  skills: [qms-management, change-control, capa-handling, audit-trail-maintenance, release-gate-enforcement]
  tools: [qms/audit-log, qms/change-control-records, provenance/log]
  inputs: [validation verdicts, threshold change requests, CAPA triggers, incident reports]
  outputs: [change-control records, CAPA records, release authorization, audit trail entries]
  autonomy: act
  kpis: [zero unauthorized threshold changes, 100% audit trail coverage, CAPA closure within SLA]
  review_gate: Director approves release authorization; CRQO approves QMS policy changes
```

**Mapped DDE artifacts:**

| Artifact | Location | Owner |
|---|---|---|
| Change-control record | `qms/ccr-{id}.json` | QMS / Change-Control Agent |
| Audit trail log | `qms/audit-log.jsonl` | QMS / Change-Control Agent |
| Release authorization | `qms/release-auth-{id}.json` | QMS / Change-Control Agent |

## 5. Evaluation Report Schema

This is the contract between AI Research and this department. All candidates must include this structure in their submission.

```json
{
  "schema_version": "1.0",
  "model_id": "string — unique model artifact identifier",
  "model_version": "string — semver or commit hash",
  "training_run_id": "string — link to provenance",
  "dataset_version": "string — must match split-registry entry",
  "split_checksum": "string — SHA-256 of test split manifest",
  "metrics": {
    "rmse": "number",
    "mae": "number",
    "r2": "number",
    "calibration_error": "number — for classification tasks",
    "monotonic_sanity": "boolean — for regression tasks where monotonicity is expected"
  },
  "thresholds_applied": {
    "r2_min": "number — default 0.5",
    "mae_max_pct": "number — default 20.0",
    "calibration_error_max": "number — default 0.10",
    "monotonic_sanity_required": "boolean — default true"
  },
  "pass_fail": "PASS | FAIL",
  "failure_reasons": ["array of strings — empty if PASS"],
  "submitted_by": "string — AI Research agent ID",
  "submitted_at": "ISO-8601 timestamp"
}
```

## 6. /api/v1/validate Endpoint Contract

| Field | Value |
|---|---|
| Method | `POST` |
| Path | `/api/v1/validate` |
| Auth | Internal service-to-service (no public access) |
| Request body | Evaluation report JSON (schema above) |
| Success response (200) | `{"verdict": "PASS", "validation_id": "uuid", "signed_at": "ISO-8601"}` |
| Failure response (200) | `{"verdict": "FAIL", "validation_id": "uuid", "reasons": [...], "signed_at": "ISO-8601"}` |
| Error response (422) | `{"detail": "schema validation error or missing fields"}` |
| Side effects | Writes to provenance log, audit trail, and (on PASS) promotes model to eligible-for-deployment |

The endpoint enforces the gate: even if called directly, it runs the same threshold checks, split integrity verification, and PCCP authorization lookup. There is no shortcut path.

---

_Published by the Regulated AI / ML-Validation department. Version 1.0._
