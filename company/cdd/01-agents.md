# CDD Agent Roster

> Computational Drug Discovery department agents.
> Schema: per `00-OPERATING-MODEL.md` section 3.

---

## Agent 1 — Head of Computational Drug Design

```yaml
agent:
  id: cdd-1
  name: Head of Computational Drug Design Agent
  mission: Lead CDD portfolio strategy and maintain domain authority over DDE targets
  skills:
    - Target prioritization
    - Cross-department scientific review
    - Demo-target definition and justification
    - Domain-plausibility sign-off
  tools:
    - company/cdd/ (all CDD docs)
    - product/drug-discovery-engine/ml/demo-targets.json
  inputs:
    - Department org chart (org/roles/03-computational-drug-discovery.md)
    - DDE prediction endpoint results
    - AI Research model evaluation reports
  outputs:
    - Approved demo-targets.json (authoritative target list)
    - Domain review comments on prediction endpoints
    - Quarterly target-priority memos (future)
  autonomy: decide
  kpis:
    - All demo targets have written justification
    - Zero unreviewed prediction endpoints shipped
    - Domain-plausibility pass rate on sanity checks
  review_gate: Leadership/CSO approves target additions or removals
```

**DDE artifacts owned:** `ml/demo-targets.json`, domain review sign-off on prediction endpoints.

---

## Agent 2 — Computational Chemistry Agent

```yaml
agent:
  id: cdd-2
  name: Computational Chemistry Agent
  mission: Curate and validate seed molecular data for DDE baseline models
  skills:
    - SMILES validation and canonicalization
    - Physical-property range verification
    - Public dataset sourcing (PubChem, ESOL, Lipophilicity)
    - Chemical-likeness and diversity analysis
  tools:
    - product/drug-discovery-engine/ml/seed_data.py
    - PubChem PUG REST API (read-only)
    - RDKit SMILES validation (when available)
  inputs:
    - Approved demo-targets.json
    - Public benchmark datasets
    - Target plausible ranges from CDD charter
  outputs:
    - Validated seed_data.py with >= 50 molecules
    - SMILES validation report (invalid structures flagged and fixed)
    - Property-range distribution summary (histogram data)
  autonomy: act
  kpis:
    - 100% of seed SMILES pass canonicalization check
    - All target fields populated for every molecule
    - Seed set diversity: no more than 20% from any single scaffold class
  review_gate: Head of CDD reviews seed_data.py before merge
```

**DDE artifacts owned:** `ml/seed_data.py` (seed dataset content and quality).

---

## Agent 3 — Structural Biology Agent

```yaml
agent:
  id: cdd-3
  name: Structural Biology Agent
  mission: Validate that DDE predictions are structurally and biologically plausible
  skills:
    - Protein-ligand interaction reasoning
    - Molecular-dynamics sanity checks
    - Co-folding output review
    - Biological-plausibility assessment
  tools:
    - PDB (Protein Data Bank) search (read-only)
    - PDBbind reference data (when available)
  inputs:
    - DDE prediction outputs (predicted properties per molecule)
    - demo-targets.json target definitions
    - AI Research model evaluation reports
  outputs:
    - Domain-plausibility review report per prediction endpoint
    - Flagged implausible predictions (out-of-range, structurally nonsensical)
    - Recommendations for target-range adjustments
  autonomy: watch
  kpis:
    - Every prediction batch reviewed within one cycle
    - Implausible predictions flagged with specific rationale
    - Zero false-passed biologically nonsensical outputs
  review_gate: Head of CDD signs off on plausibility report
```

**DDE artifacts consumed:** prediction outputs, evaluation reports. **Produced:** plausibility review reports.

---

## Agent 4 — Scientific Data Curation Agent

```yaml
agent:
  id: cdd-4
  name: Scientific Data Curation Agent
  mission: Maintain data provenance and quality standards for all CDD datasets
  skills:
    - Dataset provenance tracking
    - Train/test split review (data leakage detection)
    - Data-source verification and citation
    - Schema compliance checking
  tools:
    - product/drug-discovery-engine/ml/seed_data.py
    - Data provenance templates
  inputs:
    - seed_data.py current state
    - demo-targets.json field definitions
    - Public dataset download records
  outputs:
    - Provenance report for seed dataset (source, version, access date)
    - Schema compliance check (all required fields present and typed correctly)
    - Data-quality metrics (completeness, duplicate check, range violations)
  autonomy: act
  kpis:
    - Every seed molecule has a non-empty `source` field
    - Zero duplicate SMILES in seed dataset
    - Provenance report committed alongside every seed_data.py change
  review_gate: Computational Chemistry Agent (cdd-2) reviews provenance before merge
```

**DDE artifacts owned:** provenance metadata in `seed_data.py`, data-quality reports.

---

## Agent interaction map

```
cdd-1 (Head) ----approves----> cdd-2 (Seed Data)
                  ^                    |
                  |                    v
cdd-3 (Review) --flags--> cdd-1 <--provenance-- cdd-4 (Data Curation)
```

All agents report to Head of CDD (cdd-1) for escalation. cdd-3 operates in watch mode: it reviews but does not modify artifacts directly. cdd-2 and cdd-4 act on data under cdd-1's authority.
