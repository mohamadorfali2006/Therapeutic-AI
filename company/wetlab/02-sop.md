# Wet Lab / Biology — Standard Operating Procedure: Virtual Validation Workflow

**SOP ID:** WETLAB-SOP-001
**Scope:** Foundation phase — virtual experimental validation of DDE predictions
**Owner:** wetlab-1 (Head of Biology Agent)
**Applies to:** All agents in `company/wetlab/`

---

## 1. Purpose

This SOP defines the end-to-end workflow for validating DDE predictions without a physical wet lab. For every prediction the ML pipeline produces, we create a structured validation-claim record, design a proposed assay, define acceptance criteria, and specify the feedback loop that returns results to model retraining. The goal is to be ready for physical validation the moment lab infrastructure exists, while providing useful structure now.

## 2. Trigger

A new prediction is emitted by the DDE ML pipeline and enters the validation queue. The prediction must include:
- `model_version` (exact version string)
- Prediction type (binding affinity, solubility, toxicity, etc.)
- Predicted value or category
- Target compound/protein identifier

## 3. Workflow Steps

### Step 1: Claim Creation (wetlab-1)

Create a validation-claim record in the registry:

```
claim_id:        VC-YYYY-NNNN (sequential)
claim:           <plain-English description>
model_version:   <exact model version>
prediction:      <value or category>
proposed_assay:  <initial assay class, refined in Step 2>
expected_measured_window: <initial range, refined in Step 2>
status:          proposed
created_by:      wetlab-1
last_updated:    <timestamp>
feedback_sent:   false
```

Registry location: `company/wetlab/registry/claims.json` (or equivalent structured format).

**Gate:** Record must have all required fields. No blank `model_version`. No blank `claim`.

### Step 2: Assay Design (wetlab-2)

For each `proposed` claim, the Assay Design Agent produces an assay design document containing:

| Field | Description |
|---|---|
| Assay name | Specific assay type (e.g., "SPR binding kinetics") |
| Target | Protein or compound being tested |
| Method | Brief protocol summary |
| Instrument | Required equipment class |
| Acceptance window | Numeric range for a "pass" result |
| Rationale | Why this assay is appropriate for this prediction class |
| Estimated duration | Time from initiation to result |

The design updates `proposed_assay` and `expected_measured_window` in the claim record. Status changes to `in_design`.

**Gate:** wetlab-1 approves assay design. If the prediction class has no suitable virtual assay, status moves to `archived` with rationale.

### Step 3: Feasibility Review (wetlab-3)

The Protein Engineering Agent reviews the target protein feasibility:

- Is the protein expressible in standard systems?
- Are there stability or aggregation risks?
- Does the assay require a specific construct or tag?

Produces a feasibility report. If feasibility is `low`, wetlab-1 may reclassify the claim or add risk flags.

Status remains `in_design` or moves to `ready_for_test` if feasible.

### Step 4: QC Criteria Definition (wetlab-4)

The Bioinformatics QC Agent defines:

1. **Data capture format** — what fields the experimental result must contain to be ingested by the ML pipeline.
2. **Acceptance criteria** — statistical thresholds (e.g., CV < 15%, n >= 3 replicates).
3. **Outlier rules** — how to handle data points that fail QC.
4. **ML ingestion spec** — exact JSON/CSV schema the result must match.

Status changes to `ready_for_test` once QC criteria are approved by wetlab-1 and confirmed compatible by AI Research.

### Step 5: Protocol Finalization (wetlab-5)

The Lab Operations Agent produces:

- A versioned virtual protocol document combining the assay design, feasibility notes, and QC criteria.
- A resource estimate (even if virtual — instruments, reagents, personnel hours).
- A timeline estimate.

Status remains `ready_for_test`. The claim is now fully specified and awaiting physical execution (future phase).

### Step 6: Simulated / Retrospective Feedback (wetlab-1)

In the foundation phase, when historical data or literature values are available:

1. wetlab-1 populates a `simulated_result` field in the claim record.
2. Status changes to `measured` with a `measurement_type: simulated` annotation.
3. A feedback record is generated and sent to the ML pipeline:

```
feedback:
  claim_id: VC-YYYY-NNNN
  model_version: <must match claim>
  predicted_value: <from claim>
  measured_value: <simulated or historical>
  delta: <measured - predicted>
  within_acceptance_window: true/false
  feedback_sent: true
  sent_to: ml-retraining-pipeline
```

**Gate:** Feedback record must reference the exact `model_version` from the original claim. No generic or latest-version references.

### Step 7: Claim Closure (wetlab-1)

| Condition | Final Status |
|---|---|
| Measured value within acceptance window | `confirmed` |
| Measured value outside acceptance window | `discontinued` |
| No assay possible, archived with rationale | `archived` |
| Superseded by newer prediction | `superseded` |

All terminal-status claims remain in the registry for audit. No claims are deleted.

## 4. Feedback Loop to Model Retraining

The feedback loop is the critical path:

```
Prediction --> Claim --> Assay Design --> (Simulated) Measurement --> Feedback Record --> ML Retraining
     ^                                                                                   |
     |_________ new model_version prediction enters the loop _____________________________|
```

Rules:
- Every feedback record includes the originating `claim_id` and `model_version`.
- The ML pipeline logs the feedback event with the model version it retrains from.
- After retraining, new predictions are evaluated against the same claims to measure improvement.
- wetlab-1 reviews the delta between old and new model performance on previously claimed predictions.

## 5. Registry Maintenance

- Claims are never deleted, only terminal-statused.
- The registry is version-controlled (git).
- wetlab-1 performs a monthly registry audit: no claims stuck in `proposed` or `in_design` for more than 30 days without justification.
- Registry schema changes require wetlab-1 approval and a changelog entry.

## 6. Escalation

| Situation | Escalation path |
|---|---|
| Prediction class has no suitable assay | wetlab-1 -> wetlab-3 feasibility -> CSO |
| Feasibility assessment conflicts with assay design | wetlab-3 raises to wetlab-1 for resolution |
| QC criteria incompatible with ML ingestion format | wetlab-4 -> AI Research for format negotiation |
| Claim open > 30 days | wetlab-1 monthly audit flag -> CSO |

---

*SOP WETLAB-SOP-001 — Therapeutic-AI Wet Lab / Biology*
*Last updated: 2026-09-06*
