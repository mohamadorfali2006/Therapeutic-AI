# Regulated AI / ML-Validation — Department Charter

> The validation gate authority for every model that reaches the Drug Discovery Engine.
> This department is non-negotiable: no model, no prediction, no deployed artifact bypasses it.

## 1. Mission

Ensure every machine-learning model that serves a prediction in the DDE has been independently validated against objective, threshold-based criteria and that a complete audit trail exists linking that model to its data provenance, evaluation metrics, and authorization record. The department exists to protect patients, the company, and scientific integrity.

## 2. Scope

| In scope | Out of scope |
|---|---|
| Validation gate policy and enforcement | Model research direction and architecture choices |
| Evaluation report schema and verification | Dataset curation (owned by Data dept) |
| Regression gate definition and thresholding | Wet-lab experimental design (owned by Wet Lab) |
| PCCP modification protocol compliance | FDA submission assembly (owned by Regulatory) |
| Train/test split integrity verification | Day-to-day model training (owned by AI Research) |
| Audit trail and provenance log management | Security pen-testing (owned by Platform Eng) |

## 3. Independence Principle

This department reports to the **Chief Regulatory & Quality Officer (CRQO)** and is matrixed to the CTO for technical coordination. It does **not** report to the CTO or any team whose performance is measured by shipping velocity.

The reason is structural: validation must be independent of the pressure to ship. A team that controls both the code and the gate it passes through has a conflict of interest. This department resolves that conflict by design.

**Operational consequences:**
- The Director of ML Validation has veto authority over any model promotion.
- No agent in AI Research, Platform Eng, or Business may override a validation verdict.
- Threshold changes require a formal QMS change-control record (see `03-guardrails.md`).
- Validation resources are budgeted and staffed under the CRQO org, not CTO.

## 4. The Validation Gate

Every model artifact that enters the DDE staging or production environment **must** pass through this department's validation gate. The gate is binary: PASS or FAIL. There is no conditional, provisional, or temporary pass.

**Gate flow (high-level):**

```
AI Research submits candidate model artifact + evaluation report
    |
    v
Regulated-AI receives and queues for validation
    |
    v
Verify: locked test split integrity (no leakage)
    |
    v
Verify: metrics meet or exceed defined thresholds
    |
    v
Verify: PCCP change protocol authorization (if retraining)
    |
    v
Verdict: PASS or FAIL
    |
    +--> PASS: model artifact signed, logged to provenance, promoted
    +--> FAIL: model artifact rejected, logged, issue routed back
```

## 5. PCCP Integration

The FDA's Predetermined Change Control Plan (PCCP) guidance (final, Dec 2024) permits iterative model retraining **only** when each change follows a pre-authorized Modification Protocol. This department is the operational executor of that protocol within the DDE.

**How PCCP maps to this department:**

| PCCP concept | DDE implementation |
|---|---|
| Modification Protocol | Pre-authorized training recipe (architecture, data bounds, hyperparameter ranges) logged in provenance |
| Specification envelope | Threshold ranges in `02-sop.md` that define acceptable metric drift |
| Impact assessment | Regression gate: compare candidate model against baseline on locked test set |
| Change authorization | QMS change-control record linking training run to authorized protocol |
| Reversion plan | Baseline model artifact retained; provenance log enables instant rollback |

**Adaptive retraining** is allowed, but only within the boundaries of the Modification Protocol. A retraining run that deviates from the authorized recipe is treated as a new model candidate requiring full validation from scratch.

## 6. Regulatory Alignment

| Standard | Relevance |
|---|---|
| FDA PCCP Guidance (Dec 2024) | Adaptive AI retraining authorization |
| IEC 62304 | Software lifecycle — V&V for medical device software |
| ISO 13485 | Quality management system |
| 21 CFR Part 11 | Electronic records and signatures |
| NIST AI RMF | AI risk management framework |

## 7. Accountability

| Question | Answer |
|---|---|
| Who signs validation verdicts? | Director, ML Validation |
| Who enforces the gate in code? | `/api/v1/validate` endpoint, `ml/evaluate.py` |
| Who owns the evaluation report schema? | This department (see `01-agents.md`) |
| Who can override a FAIL? | No one without a QMS change-control record + CRQO approval |
| Who audits this department? | QMS / Change-Control Agent + external audit |

---

_Published by the Regulated AI / ML-Validation department. Version 1.0._
