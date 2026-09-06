# CDD Charter — Computational Drug Discovery Department

> Domain authority for the Drug Discovery Engine (DDE).
> Ensures every prediction, dataset, and demo target is grounded in real drug-discovery practice.

## 1. Mission

Provide the **domain expertise** that keeps DDE anchored to physically meaningful chemistry. The department owns:

- What predictive tasks the model runs and why they matter.
- The seed dataset that feeds baseline training.
- The sanity-check rules that prevent biologically implausible outputs.

CDD does not write production model code or deploy infrastructure. It defines the **what** and **validates the plausibility**; AI Research and Platform Engineering implement the **how**.

## 2. Scope boundaries

| In scope | Out of scope |
|---|---|
| Demo-target definition and justification | Model architecture decisions |
| Seed SMILES curation and validation | Training-loop implementation |
| Domain-plausibility review of predictions | FDA regulatory submission content |
| Physical-property target ranges and sanity checks | Wet-lab experiment design |
| Public dataset source identification (PubChem, etc.) | Production dataset pipelines |

## 3. Demo Targets Table

The foundation demo ships with **three** property-prediction targets. Each is clearly labeled demonstration-grade.

| # | Target | Task type | Target field | Why it matters for DDE demo | Plausible range |
|---|---|---|---|---|---|
| 1 | **logP estimate** | Regression | `logP` | Lipophilicity governs membrane permeability and oral bioavailability. A logP predictor is the canonical cheminformatics baseline; every ML-for-drug-discovery paper includes one. | -2 to 6 |
| 2 | **Aqueous solubility proxy** | Regression | `solubility_logS` | Solubility determines formulation feasibility and in-vivo absorption. The logS transform of mol/L solubility maps to a tractable regression range. | -10 to 0 |
| 3 | **Synthetic-likelihood score** | Classification (feasible / not-feasible) or ordinal | `synth_score` | A molecule the chemist cannot make is worthless regardless of predicted potency. This proxy flags synthetic accessibility, a critical filter in any generative design loop. | 0 to 10 (10 = easy) |

### Target justification notes

- **logP** and **solubility** are chosen because public gold-standard datasets exist (ESOL, Lipophilicity) enabling immediate train/test splits with known ground truth.
- **Synthetic-likelihood** is included because DDE's generative pipeline needs a synthesizability gate. For the demo, scores are computed from a rule-based heuristic (e.g., fragment-based SA score) rather than a learned model, making them deterministic and auditable.
- All three targets are explicitly **not** intended to predict clinical outcome, toxicity, or efficacy. They are physical-property proxies used to demonstrate the ML pipeline end-to-end.

## 4. Seed Dataset Spec

The seed dataset lives in `product/drug-discovery-engine/ml/seed_data.py` as an embedded Python structure (list of dicts). This avoids external file dependencies in the demo and keeps the data under version control.

| Field | Type | Source |
|---|---|---|
| `smiles` | str | PubChem CID lookup or published benchmark set |
| `logP` | float | Experimental or computed benchmark value |
| `solubility_logS` | float | ESOL dataset or equivalent |
| `synth_score` | float (0-10) | Rule-based SA scoring |
| `source` | str | Dataset provenance tag (e.g., `"ESOL-v1"`, `"PubChem-12345"`) |

Total seed count target: **50-100 molecules**. Enough to train a demonstrable regressor; small enough to embed directly.

## 5. Relationship to other departments

| Interface | Direction | Artifact |
|---|---|---|
| AI Research (`ai-research/`) | CDD provides targets + seed data; AI Research trains models | `seed_data.py`, `demo-targets.json` |
| Regulated AI (`regulated-ai/`) | CDD reviews domain plausibility of validation reports | Prediction sanity-check reports |
| Wet Lab (`wetlab/`) | Future: CDD-defined targets map to virtual assays | Target definitions |

## 6. Success criteria

- Three demo targets are defined, justified, and stored as a versioned JSON spec.
- Seed dataset contains >= 50 chemically valid SMILES with all target fields populated.
- Every prediction endpoint in DDE can be sanity-checked against the plausible-range column above.
- No CDD artifact makes claims about clinical efficacy or FDA readiness.
