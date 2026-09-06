# AI Research & ML — Standard Operating Procedures

## SOP-1: Training Pipeline

**Owner:** ai-research-4 (Predictive Modeling Scientist)
**Trigger:** Model variant approved by VP AI Research
**Inputs:** Labelled dataset (SMILES string + target value), model configuration

### Steps

1. **Load data.** Read the labelled dataset (CSV/JSON) containing SMILES strings and numeric target values.
2. **Featurise.** Pass each SMILES string through `ml/features.py` to produce a fixed-length binary fingerprint vector. No external chemistry libraries (no RDKit).
3. **Split.** Divide data into train (70%), validation (15%), test (15%) using a deterministic split with a recorded random seed. The test set is written to a separate file and is never loaded during training.
4. **Fit.** Instantiate the regressor as defined in `ml/baseline.py`. Fit on the training set only. Record the random seed and sklearn version in the artifact metadata.
5. **Persist.** Save the fitted model as a joblib artifact to `ml/artifacts/model_YYYYMMDD_vN.joblib`. Save the associated fingerprint configuration and training metadata to `ml/artifacts/model_YYYYMMDD_vN_meta.json`.
6. **Log.** Record the training run in the training log (date, seed, dataset hash, artifact path, sklearn version).

### Artifact naming convention

```
ml/artifacts/model_YYYYMMDD_vN.joblib      # model artifact
ml/artifacts/model_YYYYMMDD_vN_meta.json   # metadata (seed, fingerprint config, dataset hash)
```

### Validation checkpoint

After step 3, confirm the test set file exists and contains the expected row count. If the test set is empty or missing, halt and report.

---

## SOP-2: Evaluation Protocol

**Owner:** ai-research-5 (Evaluation Scientist) — independent from modelers
**Trigger:** New model artifact present in `ml/artifacts/`
**Inputs:** Persisted model artifact, held-out test set, evaluation configuration

### Steps

1. **Load artifact.** Load the model from `ml/artifacts/` and read its metadata JSON to confirm version and fingerprint configuration.
2. **Load test set.** Load the held-out test split. Confirm it matches the split used during training (same dataset hash, same seed).
3. **Featurise.** Apply `ml/features.py` to the test SMILES using the same configuration as training.
4. **Predict.** Generate predictions on the test set using the loaded model.
5. **Score.** Compute the following metrics:

| Metric | Target | Failure threshold |
|---|---|---|
| RMSE | Lower is better | > 2x previous best baseline |
| MAE | Lower is better | > 2x previous best baseline |
| R2 | Higher is better | < 0.5 |

6. **Calibration check.** Bin predictions vs. actuals into deciles and verify monotonicity. Flag any bin where the residual is > 3x the overall MAE.
7. **Write report.** Produce an evaluation report JSON to `ml/artifacts/evaluation_report_YYYYMMDD_vN.json` with the structure:

```json
{
  "artifact": "model_YYYYMMDD_vN.joblib",
  "dataset_hash": "<sha256 of test set>",
  "test_samples": 0,
  "metrics": {
    "rmse": 0.0,
    "mae": 0.0,
    "r2": 0.0
  },
  "calibration": {
    "bins": [],
    "monotonic": true,
    "max_bin_residual": 0.0
  },
  "evaluation_timestamp": "2026-09-06T00:00:00Z",
  "evaluator_version": "1.0.0"
}
```

8. **Verdict.** Append a pass/fail verdict based on the thresholds above. The report is the source of truth for the validation gate.

### Independence rule

The evaluation agent must not be the same agent that trained the model. If the evaluation script was modified by the modeling agent since the last VP AI Research review, flag this in the report.

---

## SOP-3: Handoff to Regulated-AI

**Owner:** ai-research-6 (Scientific ML Engineering Lead)
**Trigger:** Evaluation report contains a pass verdict
**Inputs:** Evaluation report JSON, model artifact, training metadata

### Steps

1. **Prepare handoff package.** Assemble the following into a single directory or bundle:

| Item | Path |
|---|---|
| Model artifact | `ml/artifacts/model_YYYYMMDD_vN.joblib` |
| Training metadata | `ml/artifacts/model_YYYYMMDD_vN_meta.json` |
| Evaluation report | `ml/artifacts/evaluation_report_YYYYMMDD_vN.json` |
| Feature config snapshot | Content of `ml/features.py` at commit hash |
| Baseline config snapshot | Content of `ml/baseline.py` at commit hash |
| Git commit hash | The commit at which the model was trained |

2. **Create handoff manifest.** Write `ml/artifacts/handoff_YYYYMMDD_vN.json` containing:

```json
{
  "artifact_version": "model_YYYYMMDD_vN",
  "git_commit": "<hash>",
  "files": [],
  "evaluation_report": "evaluation_report_YYYYMMDD_vN.json",
  "handed_off_by": "ai-research-6",
  "handed_off_at": "2026-09-06T00:00:00Z"
}
```

3. **Notify Regulated-AI.** Submit the handoff manifest to Regulated-AI for the validation gate. Regulated-AI will independently verify:
   - No data leakage (test split never appeared in training)
   - Reproducibility (seed + config match)
   - Evaluation report integrity (metrics match re-run)
   - Provenance chain (git history is unbroken)

4. **Await decision.** Regulated-AI returns one of: APPROVED, REJECTED, or CONDITIONAL (approved with restrictions). The model artifact is only promoted to the model registry if APPROVED.

5. **Record outcome.** Log the validation gate outcome in the training log and in `ml/artifacts/` metadata.

---

_Last updated: 2026-09-06_
