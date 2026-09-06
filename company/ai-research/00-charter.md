# AI Research & ML — Department Charter

## Mission

Design, train, and rigorously evaluate the ML models that power the Drug Discovery Engine (DDE). Our output is not a paper or a demo — it is production-grade model code and evaluation evidence that Regulated-AI can defend in a PCCP submission.

## Scope

| In scope | Out of scope |
|---|---|
| Molecular property prediction (regression) | Protein structure prediction (future phase) |
| Fingerprint featurisation (pure-Python, no RDKit) | Wet-lab experimentation |
| Training and evaluation pipelines | FDA submission assembly |
| Model artifact versioning and provenance | Deployment to production cluster |
| Calibration, OOD detection research | Commercial go-to-market |

## Product Ownership

We own `product/drug-discovery-engine/ml/` — the ML service within the DDE repo.

### Files we own directly

| File | Responsibility |
|---|---|
| `ml/features.py` | SMILES string-to-fingerprint featurisation (pure-Python, no RDKit) |
| `ml/baseline.py` | Baseline regressor: fingerprint input -> sklearn regressor, train/predict API |
| `ml/train.py` | CLI entrypoint: load data, featurise, split, fit, persist artifact to `ml/artifacts/` |
| `ml/evaluate.py` | Evaluation protocol: RMSE / MAE / R2 on held-out test set, calibration checks, JSON report |

### Files we contribute to (shared ownership)

| File | Our contribution |
|---|---|
| `app/routers/prediction.py` | Model loading and inference contract |
| `ml/artifacts/` | Versioned model artifacts (joblib) and evaluation reports |

## The Research Loop

```
 1. Design          2. Train           3. Evaluate        4. Handoff
 +-----------+     +-----------+     +--------------+   +--------------+
 | Scientist  |     | train.py   |     | evaluate.py   |   | Evaluation   |
 | proposes   | --> | fits model | --> | scores on     |-->| report JSON  |
 | model      |     | persists   |     | held-out test |   | handed to    |
 | variant    |     | artifact   |     | set           |   | Regulated-AI |
 +-----------+     +-----------+     +--------------+   +--------------+
       ^                                                           |
       +--- iterate if metrics below threshold -------------------+
```

1. **Design.** A scientist proposes a model variant (new hyperparameters, different fingerprint radius, alternative regressor). The variant is specified as a change to `ml/baseline.py` or `ml/features.py`.
2. **Train.** `ml/train.py` is executed. It loads labelled SMILES data, featurises via `ml/features.py`, splits train/val/test, fits the model, and persists the artifact to `ml/artifacts/`.
3. **Evaluate.** `ml/evaluate.py` loads the persisted artifact and the held-out test set, computes RMSE / MAE / R2, runs calibration checks, and writes an evaluation report JSON to `ml/artifacts/`.
4. **Handoff.** The evaluation report is handed to **Regulated-AI** for the validation gate. Regulated-AI verifies provenance, checks for data leakage, and either approves or rejects the artifact. Approved artifacts are eligible for the model registry in `app/`.

## Key Principles

- **Evaluation independence.** The agent that trains a model never evaluates it. Evaluation scientists produce the score; modelling scientists cannot override it.
- **No test leakage.** The test split is never visible to the training code. This is enforced by `ml/train.py` (split happens before fit) and verified by Regulated-AI.
- **Reproducibility.** Every training run records the random seed, the full feature vector configuration, and the sklearn version. A run with the same inputs must produce the same artifact.
- **Plain-Python baseline.** The current baseline uses only pure Python and scikit-learn. No RDKit, no deep learning frameworks. This keeps the barrier to review low and the PCCP evidence simple.

## Reporting Line

AI Research & ML reports to the **CTO**. The department lead is the **VP AI Research Agent** (`ai-research-1`).

---

_Last updated: 2026-09-06_
