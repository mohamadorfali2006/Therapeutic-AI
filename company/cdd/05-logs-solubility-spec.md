# 05-LOGS-SOLUBILITY-SPEC — logS Aqueous Solubility Proxy Target

> STATUS: Demonstration-grade | NOT for clinical or regulatory use
> DEPARTMENT: Computational Drug Discovery (CDD)
> PRODUCT: Drug Discovery Engine (DDE)

---

## 1. Why aqueous solubility

Aqueous solubility is the **first ADME barrier** in early-stage drug discovery. A compound that cannot dissolve in aqueous media cannot reach systemic circulation regardless of its potency. Solubility directly governs:

- **Formulation feasibility** — the dose form (tablet, capsule, IV) requires a minimum dissolved concentration at physiological pH.
- **Oral bioavailability** — the fraction of an oral dose that reaches the bloodstream is bounded by the compound's solubility in gastrointestinal fluid.
- **Dosing window** — poorly soluble compounds require higher excipient loads, larger pills, or specialized delivery, all of which narrow the therapeutic window.

Including a solubility proxy in the DDE demo ensures the pipeline exercises a physically meaningful property that any drug-discovery ML system must address.

## 2. Why logS proxy (deterministic, cheap, demo-grade)

The target is **logS**, defined as log10 of molar aqueous solubility (mol/L) at 25 °C and neutral pH. The logS transform is preferred over raw solubility for three reasons:

1. **Tractable regression range** — logS values for drug-like molecules typically fall between -10 and 0, a range well-suited to regression models without extreme scaling.
2. **Deterministic baseline** — the demo logS values are approximate literature landmarks, not model outputs. They are fixed, auditable, and reproducible without any ML inference.
3. **Cheap to curate** — logS values for common organic compounds are widely reported in handbooks and public databases (ESOL dataset, Delaney 2004), requiring no proprietary data or wet-lab resources.

This proxy is explicitly **not** a substitute for experimental solubility measurement or pharmacokinetic modeling. It exists to demonstrate that the DDE pipeline can learn and predict a physically grounded continuous property.

## 3. 56-compound coverage strategy

The seed dataset contains **56 compounds** selected to span the chemical space relevant to early-discovery solubility filtering:

| Property spread | Examples | logS range |
|---|---|---|
| Small polar / H-bonding | Ethanol, acetic acid, acetone | -0.1 to -0.3 |
| Small alcohols and amines | 2-propanol, cyclohexylamine | -0.1 to -1.8 |
| Aromatic with polar substituents | Phenol, aniline, benzoic acid | -0.5 to -1.5 |
| Moderate lipophilic aromatics | Toluene, chlorobenzene, bromobenzene | -2.4 to -2.9 |
| Polycyclic aromatics | Naphthalene, biphenyl, anthracene | -3.6 to -4.8 |
| Alkanes | Hexane, octane | -3.9 to -4.7 |
| Heterocycles | Pyridine, pyrimidine, thiophene, piperidine | -0.7 to -1.6 |
| Halogenated small molecules | Chloroethane, bromoethane, iodoethane | -1.3 to -2.0 |
| Sulfonyl / nitrile | DMSO, acetonitrile, sulfanilamide | -0.4 to -1.3 |
| Trifluoromethyl aromatics | (Trifluoromethyl)benzene | -2.9 |

The dataset intentionally covers **polar → lipophilic** to ensure the regression model must learn a real solubility gradient rather than memorizing a narrow cluster.

## 4. CDD labeling standard

This document and all downstream CDD artifacts carry the standard labeling header per guardrail rule 9 (see `company/cdd/03-guardrails.md`):

```
STATUS: Demonstration-grade | NOT for clinical or regulatory use
DEPARTMENT: Computational Drug Discovery (CDD)
PRODUCT: Drug Discovery Engine (DDE)
```

## 5. Acceptance criteria

| Criterion | Requirement | Verified by |
|---|---|---|
| Dataset versioned | Version tag recorded in provenance doc (`company/data/05-logs-provenance.md`) | Data Ops |
| Immutable | SMILES list and target values frozen at release; no silent edits | Git history, SHA-256 |
| Deterministic | `load_seed_data()` returns identical list on every call, no randomness | Module docstring, test |
| SMILES valid | All 56 SMILES parseable, no undefined atoms, no salts | CDD guardrails (`03-guardrails.md` rule 2) |
| Coverage sufficient | Polar-to-lipophilic spread confirmed by logS range | `target_range()` output |
| Research-only caveat | Present in module docstring and spec header | Code review |

## 6. Relationship to other DDE targets

| Target | Relationship to logS |
|---|---|
| logP (lipophilicity) | Inverse correlation: higher logP generally implies lower logS. Together they describe the hydrophilic–lipophilic balance critical for membrane permeation vs. dissolution. |
| Synthetic-likelihood | Independent; a compound may be easy to synthesize yet poorly soluble, and vice versa. Both are necessary filters in a generative pipeline. |

---

_Spec authored by CDD department. Reviewed quarterly by Head of CDD; annually by CSO._
