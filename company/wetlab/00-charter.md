# Wet Lab / Biology Department — Charter

**Department:** `wetlab/` — Wet Lab / Biology
**Reports to:** CSO
**Product scope:** Experimental validation of DDE predictions (virtual phase)

## 1. Purpose

The Wet Lab / Biology department exists because the Drug Discovery Engine makes testable predictions. Our purpose is to define, document, and enforce the bridge between computational prediction and experimental confirmation. In the FOUNDATION phase there is no physical wet lab — we define the **virtual experimental validation protocol**, a documented contract describing how AI predictions would be confirmed by experiment through a design-build-test-learn loop, and maintain a **validated claims registry** that tracks every prediction through to measured status.

## 2. Scope (Foundation Phase)

| In scope | Out of scope |
|---|---|
| Virtual validation protocol definition | Physical assay execution |
| Assay design proposals for each prediction class | Instrument procurement or lab buildout |
| Validated claims registry schema and population | Real experimental data generation |
| Feedback loop specification (results -> model retraining) | Wet-lab staff hiring or biosafety |
| Acceptance window definitions per assay type | Clinical sample handling |

## 3. Experimental Validation Contract

The validation contract is the formal agreement between the DDE ML pipeline and experimental biology. It specifies:

1. **For each prediction**, the wet lab produces a validation-claim record (see `02-sop.md`).
2. **Each claim** names a proposed assay, an expected measured window, and acceptance criteria.
3. **No claim** is marked "confirmed" without physical measurement data — virtual-only claims use status `proposed` or `simulated`.
4. **Feedback loop**: when physical data arrives, results flow back to the ML team with the exact `model_version` referenced, enabling targeted retraining and evaluation.

The contract will live at `product/drug-discovery-engine/docs/VALIDATION-CONTRACT.md` as the product-level spec. This department owns the biology rationale and assay design that feeds that contract.

## 4. Design-Build-Test-Learn Loop

```
  DDE Prediction
       |
       v
  [DESIGN]  Assay Design Agent proposes assay, acceptance window
       |
       v
  [BUILD]   Lab Ops Agent prepares virtual protocol, resource plan
       |
       v
  [TEST]    Bioinformatics QC Agent defines data capture and QC criteria
       |
       v
  [LEARN]   Head of Biology reviews claim, routes feedback to ML
       |
       v
  Model Retraining (with exact model_version reference)
```

Each stage produces a documented artifact. No stage is skipped. The loop is not complete until feedback reaches the ML pipeline with a traceable `model_version`.

## 5. Validated Claims Registry

A structured registry (schema in `00-charter.md` and detailed in `02-sop.md`) that tracks every prediction entering validation. Fields:

| Field | Description |
|---|---|
| `claim_id` | Unique identifier (e.g., `VC-2026-0001`) |
| `claim` | Plain-English description of the prediction |
| `model_version` | Exact model version that produced the prediction |
| `prediction` | Numeric or categorical prediction value |
| `proposed_assay` | Name/class of proposed experimental assay |
| `expected_measured_window` | Acceptable range for physical measurement |
| `status` | `proposed` / `in_design` / `ready_for_test` / `measured` / `confirmed` / `disconfirmed` |
| `feedback_sent` | Boolean — whether results were returned to ML pipeline |
| `created_by` | Agent or human who initiated the claim |
| `last_updated` | Timestamp of most recent status change |

## 6. Key Principles

1. **Honesty first.** All foundation-phase claims are virtual. No claim may represent itself as physically measured.
2. **Traceability.** Every claim links to a specific `model_version`. Every feedback event references the originating claim.
3. **Reproducibility.** Assay designs must be detailed enough that a second agent (or human scientist) could execute them independently.
4. **Closure.** Every claim must reach a terminal status (`confirmed`, `disconfirmed`, or `archived`). No open-ended claims.

## 7. Relationship to Other Departments

| Department | Interaction |
|---|---|
| AI Research / ML | Receives predictions; sends feedback with `model_version` |
| Computational Drug Discovery | Provides biological context for assay design |
| Regulated AI / ML-Validation | Co-signs validation contracts touching regulated claims |
| Data & Infrastructure | Provides storage for claim registry and assay data |

---

*Department charter — Therapeutic-AI Wet Lab / Biology*
*Last updated: 2026-09-06*
