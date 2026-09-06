# Product Status — DDE v0.2

**Product:** Drug Discovery Engine (research platform foundation)
**Status:** Foundation tier, research-use only — NOT a medical device
**DDE API version:** 0.2.0

## Current capabilities (v0.2)
- **Predict** logP (octanol/water) or logS (aqueous solubility proxy, log mol/L)
  for small-molecule SMILES via `/api/v1/predict` (property-routed models).
- **Validate** the model suite on locked test splits via `/api/v1/validate`
  (per-model gate; thresholds: R2 >= 0.50, MAE <= 20% of range).
- **Trace** every prediction via append-only provenance (`/api/v1/traces/{id}`).
- **List** registered models via `/api/v1/models`.
- Web dashboard with predict/trace/models UI, dark + light theme.

## Regulatory posture
- Dual-track: discovery research (current, non-SaMD) and future FDA-cleared SaMD.
- Current output is **research-use only**: demonstration-grade model predictions.
- Adaptive retraining under a PCCP-first posture is a future, pre-authorized
  capability — not enabled in v0.2.
- All predictions and validation verdicts are logged with immutable provenance
  to support future 510(k)/De Novo evidence building.

## Compliance reminders for engineering
- No medical claims in UI or copy (enforced: "Research Use Only — Not a Medical Device").
- Data provenance + train/test separation are non-negotiable.
- Never log PHI; no secrets in repo.

_Last reviewed: 2026-09-06 (Sprint 1 gate review)._