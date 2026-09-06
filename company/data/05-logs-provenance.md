# 05-LOGS-PROVENANCE — logS Dataset v2 Provenance Record

> STATUS: Demonstration-grade | NOT for clinical or regulatory use
> DEPARTMENT: Data & Infrastructure
> PRODUCT: Drug Discovery Engine (DDE)

---

## 1. Dataset identity

| Field | Value |
|---|---|
| Dataset name | `logs_seed` |
| Version tag | `seed-2026.09.06-v2` |
| Record count | 56 molecules |
| Target property | logS (aqueous solubility proxy, log mol/L) |
| Module path | `product/drug-discovery-engine/ml/logs_data.py` |
| Spec path | `company/cdd/05-logs-solubility-spec.md` |

## 2. Source of values

All 56 logS values are **approximate literature landmarks** drawn from published aqueous solubility data for common organic compounds. They are labeled **research-use only** and are not derived from any model, algorithm, or wet-lab experiment conducted by Therapeutic-AI.

The values serve as physically consistent regression targets: polar and hydrogen-bonding compounds carry higher (less negative) logS values, while larger nonpolar and lipophilic compounds carry lower (more negative) values, consistent with established structure–solubility relationships.

## 3. Curation policy

1. **SMILES source**: The 56 SMILES strings are identical to those in `product/drug-discovery-engine/ml/seed_data.py`. No SMILES were added, removed, or reordered relative to the logP seed dataset.
2. **logS assignment**: Each compound's logS is an approximate landmark value consistent with published aqueous solubility data for that compound or a closely related analogue. Values are not experimental measurements from Therapeutic-AI.
3. **Polarity check**: LogS values are monotonic with expected polarity — polar/H-bonding compounds (ethanol, acetic acid, acetonitrile) have higher logS; lipophilic aromatics and alkanes have lower logS. This cross-check ensures physical consistency.
4. **No fabrication**: No value was invented to fit a model or produce a desired training outcome. All values are anchored to published literature ranges.

## 4. Immutability statement

Once released as `seed-2026.09.06-v2`, the SMILES list and logS values in `logs_data.py` are **immutable**. Any correction requires:

1. A new entry in this provenance record (append-only) referencing the original version.
2. A new version tag (e.g., `seed-YYYY.MM.DD-v3`).
3. The old version remains in git history; it is never overwritten or deleted.

This immutability is enforced by Data Ops through code review and the append-only provenance convention (see `company/data/03-guardrails.md` rule R3).

## 5. Ownership

| Role | Responsibility |
|---|---|
| CDD curator | Defines the target property, selects the compound set, assigns logS values, validates physical consistency |
| Data Ops | Enforces versioning, immutability, and provenance record integrity |
| CTO | Final escalation authority for provenance disputes |

## 6. File paths

| File | Purpose |
|---|---|
| `product/drug-discovery-engine/ml/logs_data.py` | Deterministic, self-contained seed dataset (56 tuples) |
| `company/cdd/05-logs-solubility-spec.md` | CDD domain specification for the logS target |
| `company/data/05-logs-provenance.md` | This provenance record |

## 7. Version history

| Version | Date | Change |
|---|---|---|
| `seed-2026.09.06-v2` | 2026-09-06 | Initial release: 56 molecules with approximate logS literature landmarks |

---

_Provenance record authored by Data Ops. Append-only; corrections add new rows, never edit existing ones._
