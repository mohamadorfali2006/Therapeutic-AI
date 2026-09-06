# Regulated AI / ML-Validation — Guardrails and Enforcement Rules

> Non-negotiable rules that govern the validation gate. Every agent in this department
> and every external agent interacting with the validation system must follow these rules.
> Violations are incidents, not discussions.

## 1. Separation of Duties — No Self-Serving Validation

**Rule:** The agent that trains a model **cannot** be the agent that validates it.

| Enforcement | Detail |
|---|---|
| Who trains | AI Research agents (ai-research/ dept) |
| Who validates | Regulated AI agents (this department) |
| Why | A team that trains a model has a natural incentive to see it pass. Independence eliminates this conflict. |
| Implementation | `/api/v1/validate` requires a caller identity; the system rejects validation requests from the same agent_id that submitted the training run |
| Exception | None. Even the Director cannot validate their own model if they happen to train one. |

**Concrete mapping:** In the DDE codebase, `ml/evaluate.py` is called by the V&V Test Engineer Agent's pipeline, not by AI Research's training pipeline. The two pipelines run in separate execution contexts.

## 2. Threshold Integrity — No Retroactive Lowering

**Rule:** Validation metric thresholds cannot be lowered, widened, or made more permissive without a formal QMS change-control record.

| Enforcement | Detail |
|---|---|
| Current defaults | R2 >= 0.5, MAE <= 20% of target range, calibration_error <= 0.10, monotonic_sanity = TRUE |
| To change | QMS Agent creates a change-control record (CCR), Director approves, CRQO signs off |
| Audit | Every threshold value in every validation verdict is logged. Any discrepancy between the declared threshold in the verdict and the currently authorized threshold is an anomaly. |
| Anti-retroactive | Thresholds applied to a validation verdict are frozen at verdict time. Changing the threshold afterward does not retroactively change the verdict. |

**Change-control procedure for threshold changes:**

```
1. Requester submits threshold change request to QMS Agent
2. QMS Agent creates CCR with: current value, proposed value, justification, risk assessment
3. Director reviews and approves or rejects
4. If approved: CRQO signs off
5. QMS Agent updates SOP-REG-001 §3 Step 3 thresholds
6. QMS Agent logs CCR in qms/audit-log.jsonl
7. Old threshold remains active until new CCR is fully signed
8. No interim or provisional thresholds allowed
```

## 3. Leaked Test Dataset — Automatic Fail and Quarantine

**Rule:** If the test split integrity check (Step 2 of SOP-REG-001) detects any form of data leakage, the result is an automatic FAIL with immediate quarantine. No human override, no exception, no "it's probably fine."

| Leakage type | Detection method | Consequence |
|---|---|---|
| ID overlap | Same sample IDs in train and test sets | FAIL + quarantine model artifact + quarantine test split |
| Feature-vector duplication | Identical feature vectors across train and test | FAIL + quarantine model artifact + quarantine test split |
| Checksum mismatch | Test split checksum does not match split-registry | FAIL + quarantine model artifact |
| Split file tampering | File hash changed since registry recording | FAIL + quarantine model artifact + trigger incident |

**Quarantine procedure:**

1. Model artifact moved to `provenance/quarantine/` with quarantine tag.
2. Test split flagged in `data/split-registry.json` as `status: quarantined`.
3. QMS Agent opens a CAPA record.
4. AI Research notified with specific leakage details.
5. Training must restart with a clean, verified split.

## 4. Audit Trail Mandatory

**Rule:** Every action taken by any agent in this department must be logged with timestamp, agent identity, action taken, and input/output references.

| What is logged | Where | Format |
|---|---|---|
| Validation reception | `qms/audit-log.jsonl` | JSON line: `{ts, action: "received", agent, model_id}` |
| Split integrity check | `qms/audit-log.jsonl` + `reports/split-integrity-*.json` | JSON |
| Metrics threshold check | `qms/audit-log.jsonl` + `reports/vv-test-report-*.json` | JSON |
| PCCP authorization check | `qms/audit-log.jsonl` | JSON line |
| Validation verdict | `qms/audit-log.jsonl` + `provenance/validation-verdicts.json` | JSON |
| Any override or exception | `qms/audit-log.jsonl` + `qms/incidents/` | JSON + incident record |

**Audit trail integrity:**
- Log files are append-only (the system must not allow editing or deletion of log entries).
- Each log entry includes a SHA-256 hash of the previous entry (chain-of-custody pattern).
- Log files are backed up to a separate location on every write.

## 5. Bypass = Incident

**Rule:** Any attempt to bypass, circumvent, or shortcut the validation gate is a reportable incident.

**What constitutes a bypass:**

| Bypass | Example |
|---|---|
| Direct model promotion | Deploying a model to production without calling `/api/v1/validate` |
| Forced verdict | Modifying the verdict record after signing |
| Endpoint misuse | Calling the validate endpoint with fabricated metrics |
| Split manipulation | Altering the test split to improve model scores |
| Threshold override | Changing thresholds in code without a CCR |
| Identity circumvention | Using another agent's identity to validate your own model |

**Incident response:**

1. Detection triggers an immediate halt to the affected pipeline.
2. QMS Agent opens an incident record in `qms/incidents/`.
3. CRQO is notified within one incident cycle.
4. Root cause analysis is mandatory before resumption.
5. If patient safety could be affected, the Regulatory department is engaged per FDA reporting obligations.
6. The incident record becomes part of the permanent audit trail.

## 6. Evidence of Compliance

| Guardrail | Evidence artifact | Verification frequency |
|---|---|---|
| Separation of duties | `qms/audit-log.jsonl` entries showing agent identities differ | Every validation run |
| Threshold integrity | CCR records in `qms/` + threshold values in verdicts matching SOP | Every threshold change + periodic audit |
| Test split integrity | `reports/split-integrity-*.json` with pass/fail | Every validation run |
| Audit trail | `qms/audit-log.jsonl` chain integrity (hash verification) | Daily automated check |
| No bypass | Provenance log shows every production model has a PASS verdict | Every deployment |

## 7. Version Control

This document is version-controlled. Changes to guardrails require the same QMS change-control process as threshold changes. The current version is `03-guardrails.md` v1.0 in the `company/regulated-ai/` directory.

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0 | 2026-09-06 | Initial guardrails | Director, ML Validation |

---

_Guardrails v1.0 — Regulated AI / ML-Validation department. These rules are enforced, not suggested._
