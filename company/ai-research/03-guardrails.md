# AI Research & ML — Guardrails

Non-negotiable rules for all AI Research & ML work. A guardrail violation halts the pipeline and triggers an incident report to Regulated-AI.

## G1 — No Test Split Leakage

- The held-out test set is written to a separate file at split time and is **never loaded by the training pipeline** (`ml/train.py`).
- Training code must not read, import, or reference the test split file.
- The test split is only read by `ml/evaluate.py`.
- Anyone caught training on test data causes an immediate incident report and re-evaluation of the entire artifact lineage.

## G2 — Reproducible Seeds

- Every training run records the random seed in the artifact metadata (`ml/artifacts/model_*_meta.json`).
- The same seed, same dataset, same fingerprint config, and same sklearn version must produce a **bit-identical artifact**.
- If two runs with identical inputs produce different artifacts, the run is flagged as non-reproducible and rejected.
- The sklearn version and Python version are recorded in metadata at every run.

## G3 — Artifact Versioning

- Every artifact uses the strict naming convention `model_YYYYMMDD_vN.joblib`. Version `N` increments monotonically; never overwrite an existing artifact.
- Every artifact carries a metadata JSON containing: seed, dataset hash, fingerprint config, sklearn version, Python version, git commit, and timestamp.
- The dataset is hashed (sha256) at load time and the hash is stored in artifact metadata. A dataset change that alters the hash produces a new artifact version.
- Never delete or mutate a committed artifact. Supersession happens by writing a newer version, never by editing an old one.

## G4 — No Fake Metrics

- Evaluation metrics are computed exclusively by `ml/evaluate.py`, owned by the independent Evaluation Scientist (ai-research-5).
- Metrics are never hand-entered, hardcoded, or asserted before the evaluation script runs.
- The evaluation report JSON must be reproducible: re-running evaluation on the same artifact + test split yields the same numbers.
- Any agent reporting metrics that do not match the evaluation report output is in violation. This rule exists to keep the research loop honest and the PCCP evidence defensible.

## G5 — Evaluation Independent of Modeling

- The agent that trains a model (ai-research-4) may never evaluate it. Evaluation is performed by ai-research-5.
- Modeling agents have read access to evaluation results but cannot modify `ml/evaluate.py` or the output report without VP AI Research review.
- If the evaluation script is edited, the change must be reviewed by ai-research-5 and VP AI Research, and the reviewer recorded in git history.
- A model artifact cannot be presented to Regulated-AI without an evaluation report produced by ai-research-5.

## G6 — Provenance and Traceability

- Every artifact traces to a git commit. The commit hash is embedded in artifact metadata and in the handoff manifest.
- Every evaluation report references the artifact version and the dataset hash it was scored against.
- Any gap in the provenance chain (missing commit, missing metadata, unhashed dataset) blocks Regulated-AI approval.

## G7 — Escalation on Violation

- Guardrail violations are reported to the VP AI Research Agent immediately and escalated to Regulated-AI.
- A violation does not get silently fixed and moved on. The cause is recorded in `company/ai-research/` and the affected artifacts are quarantined.
- Quarantined artifacts are excluded from the model registry until the violation is fully resolved and re-validated.

## Guardrail Reference Table

| ID | Rule | Enforced where | Violation action |
|---|---|---|---|
| G1 | No test split leakage | `ml/train.py` + Regulated-AI audit | Incident report, quarantine |
| G2 | Reproducible seeds | `ml/train.py`, artifact metadata | Reject non-reproducible run |
| G3 | Artifact versioning | `ml/train.py`, metadata check | Prohibit overwrite, new version |
| G4 | No fake metrics | `ml/evaluate.py` ownership | Incident report |
| G5 | Independent evaluation | Ownership split (ai-research-4 vs 5) | Require review + re-run |
| G6 | Provenance and traceability | Metadata + git history | Block approval |
| G7 | Escalation on violation | Department lead + Regulated-AI | Quarantine affected artifacts |

---

_Last updated: 2026-09-06_
