# 03-GUARDRAILS — Data & Infrastructure rules

Non-negotiable constraints for the department. A violation blocks the artifact until fixed; repeat violations escalate to Head of Data, then CTO.

## R1. No unversioned datasets

- Every dataset used by a model or pipeline carries a declared `dataset_version` and a SHA-256 checksum in the registry.
- A dataset without a version record is not a dataset; it is scratch input and is never referenced by a model version.
- Guard: `ml/seed_data.py` refuses to emit splits for an unversioned, unchecksummed input.

## R2. No test-data leakage

- The test split is frozen at creation, checksummed, and never included in training or validation, directly or transitively.
- Helm: no hyper-parameter tuning on test metrics, no duplicate/molecule-cluster deduplication after the split, no re-splitting to "improve" results.
- The same dataset_version that produced the split must back every `model_version` trained from it; ancestry is recorded in the provenance store.
- Guard: CI verifies test-set file hash against the manifest and that `test.csv` is byte-identical to the stored fragment.

## R3. Provenance records are immutable and append-only

- A trace is written once and never edited, deleted, or merged in place. Correcting an error = writing a new record that references the original `trace_id`.
- The provenance store (`app/store.py`) rejects updates/deletes on the write path by design; file permissions and the SQLite API enforce it.
- Guard: CI loads every JSON record and asserts no duplicate/overwritten `trace_id`.

## R4. No secrets in committed files

- `.env` never enters git. Only `.env.example` with placeholder, non-secret values is committed.
- Secrets (API keys, DB credentials, signing keys) come from environment/secret store at runtime.
- Guard: CI scans for known secret patterns and forbids committing files matching `.env` (not `.env.example`). Repository scanning of `.env` is a hard block.

## R5. Every model artifact is tied to an exact dataset version

- No orphan weights: every registered `model_version` references exactly one `dataset_version` (train) and one locked eval split (val/test).
- A model whose training dataset version cannot be resolved in the registry is not shippable and is excluded from validation gates.
- Guard: the validation gate (Regulated-AI) refuses to sign off a model missing dataset ancestry in the provenance store.

## R6. Reproducibility before shipping

- Any pipeline, split, or store change must regenerate deterministically from pinned inputs on a fresh checkout; CI is the proof, not a claim.
- Regeneration must never mutate a locked test set or an existing trace.

## Violation handling

1. Log the violation in the guardrail violations log with the artifact reference and commit.
2. Block the artifact; do not merge, do not ship.
3. Fix root cause, re-verify per SOPs, record the correction (append-only) if any traces are implicated.
4. Escalate to Head of Data for systemic root-causes; CTO for cross-department impact.