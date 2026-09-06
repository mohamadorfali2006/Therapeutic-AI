# Virtual experimental validation contract — Drug Discovery Engine

Owned by `company/wetlab` + ratified by `company/regulated-ai`.

## Purpose
Defines how DDE predictions map to experimental validation (design → build →
test → learn). Foundation phase: **virtual** — records carry `measurement_type:
simulated` until physical measurement exists.

## Claim registry schema
| Field | Type | Notes |
|---|---|---|
| claim_id | str | unique, immutable |
| model_version | str | must match a registered artifact version |
| dataset_version | str | exact dataset snapshot |
| input_smiles | str | queried molecule |
| predicted_value | float | model output |
| proposed_assay | str | planned experiment (e.g., shake-flask logP) |
| acceptance_window | [lo, hi] | expected measured range around prediction |
| measurement_type | str | `simulated` (foundation) or `physical` (future) |
| status | str | `proposed` / `simulated` / `confirmed` (needs physical) |
| created_at | str | ISO timestamp |

## Feedback loop
Every model retraining tick MUST consume the claim registry:
new batch predictions → produce claims → (virtual) simulated results →
close the loop into `ml/seed_data.py` v-next. No loop without exact
`model_version` binding (blank/generic versions are quarantined).

## Guardrails (wetlab + regulated-ai joint)
1. No claim ever reaches `confirmed` without a physical measurement.
2. No fabricated experimental results — simulated results are labeled.
3. Registry is append-only, audit-trailed.
4. Any bypass of the validation gate = incident.