# CDD Guardrails

> Hard rules that no CDD agent may violate. Violations require immediate rollback and CSO notification.

---

## 1. No fabricated biology claims

- CDD outputs must never assert that a molecule is "safe," "effective," "toxic," or has any clinical or therapeutic property.
- All demo targets are explicitly labeled **demonstration-grade** and **not intended for clinical decision-making**.
- Phrases to avoid in any CDD artifact: "FDA-validated," "clinically proven," "drug candidate," "therapeutic potential."
- Phrases to use instead: "demo target," "proxy property," "baseline predictor," "for demonstration purposes only."

## 2. Seed data must be chemically valid SMILES

Every SMILES string in `seed_data.py` must satisfy:

| Rule | Check method | Failure action |
|---|---|---|
| Parseable (no syntax errors) | SMILES parser (RDKit or fallback) | Remove molecule or fix syntax |
| No undefined atoms outside {C,N,O,S,P,F,Cl,Br,I,H} | Atom-type scan | Remove molecule |
| No undefined stereochemistry markers (`[?]`) | String scan | Remove or specify stereochemistry |
| No salts or counterions (prefer neutral forms) | Fragment detection | Remove salt portion or exclude |
| Canonical form (no duplicate representations) | Canonicalization + dedup | Keep one canonical form, discard duplicate |

A molecule that fails any rule is either corrected or excluded. No unvalidated SMILES enters the seed dataset.

## 3. Demo targets are demonstration-grade only

- Every demo target must carry `"demo_only": true` in `demo-targets.json`.
- Every public-facing DDE artifact that displays a prediction must include a disclaimer:
  **"This is a demonstration prediction. It is not validated for clinical or regulatory use."**
- CDD agents must never cite a demo target as evidence of model readiness for FDA submission or any regulated use.
- The `demo_only` flag is the single source of truth. If a target is ever considered for production use, it must go through a formal re-validation process owned by Regulated AI, not CDD.

## 4. No external file dependencies in seed data

- `seed_data.py` must be self-contained: an embedded Python list-of-dicts. No reads from CSV, JSON, or network at import time.
- This ensures the demo is reproducible offline and under version control without external data fetches.

## 5. Provenance is mandatory

- Every molecule in the seed dataset must have a non-empty `source` field naming the origin (dataset name, PubChem CID, or `"computed-<method>"`).
- No fabricated provenance. If the source is unknown, the molecule is excluded.
- The provenance report is committed alongside every seed_data.py change.

## 6. Train/test separation

- Seed data must not contain the same molecule in both training and test splits.
- When the seed set is split, the split must be recorded (which molecules are train, which are test) and committed.
- This rule exists to prevent inflated accuracy claims that would undermine scientific credibility.

## 7. No secrets or credentials in CDD artifacts

- PubChem API access is anonymous (no API key needed). CDD agents must never embed API keys, tokens, or credentials in any file.
- If a future data source requires authentication, credentials go in environment variables only, never in code or docs.

## 8. Escalation path

| Violation severity | Example | Action |
|---|---|---|
| Critical | Fabricated biology claim in public artifact | Immediate rollback, CSO notification, root-cause review |
| Major | Invalid SMILES in seed dataset | Correct or exclude within current work cycle, log in provenance report |
| Minor | Missing source tag on one molecule | Fix in next seed-data update, no rollback needed |

## 9. Labeling standard

Every CDD deliverable (target spec, seed data, plausibility report) must include this header or equivalent:

```
STATUS: Demonstration-grade | NOT for clinical or regulatory use
DEPARTMENT: Computational Drug Discovery (CDD)
PRODUCT: Drug Discovery Engine (DDE)
```

This labeling is non-optional and must survive into any downstream document or presentation that incorporates CDD content.

---

_Guardrails are reviewed by the Head of CDD (cdd-1) quarterly and by CSO annually._
