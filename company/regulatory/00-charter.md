# Regulatory, Quality & Clinical — Department Charter

## Mission

Establish and maintain the regulatory posture, quality management system, and clinical evidence framework for Therapeutic-AI's Drug Discovery Engine (DDE) and its future FDA-cleared SaMD offerings. Ensure every product state — from research tool to cleared device — is accurately represented, documented, and compliant with applicable regulations.

## Scope

This department owns:

- US and EU regulatory strategy and submission readiness
- ISO 13485-aligned QMS design and audit readiness
- IEC 62304 software lifecycle alignment
- Clinical and validation evidence generation
- Regulatory labeling, disclaimers, and claims review
- CAPA (Corrective and Preventive Action) processes
- Audit trail integrity for model releases and QMS records

## Regulatory Roadmap

The DDE passes through three regulatory states. Every agent and artifact must reflect the current state accurately.

### NOW — Research Platform (current)

| Attribute | Status |
|---|---|
| Classification | Non-SaMD, research-use-only software |
| Intended use | Internal R&D, target identification, compound screening |
| Users | Therapeutic-AI researchers and computational scientists |
| Regulatory burden | Minimal — no FDA/MDR submission required |
| Required labeling | Disclaimer visible in product UI at all times |
| Data posture | Internal datasets, no PHI, no clinical decision support |

**Mandatory UI disclaimer:** `"For research use only. Not a medical device."`

This string must appear on every page of the DDE web dashboard, persistently and unremovable by end users.

### NEXT — Validation & Pre-Submission

| Attribute | Target |
|---|---|
| Activities | Formal validation studies, V&V execution, Q-Submission with FDA |
| QMS | ISO 13485 QMS operational; IEC 62304 lifecycle documented |
| Clinical | Validation study protocols, dataset lock, bias evaluation |
| Regulatory | Q-Sub meeting request, predicate search, gap analysis |
| Evidence | Regression reports, calibration records, OOD detection results |

### SaMD — FDA-Cleared Device

| Attribute | Target |
|---|---|
| Pathway | 510(k) (substantial equivalence) or De Novo (first-in-class) |
| Adaptive AI | PCCP (Predetermined Change Control Plan) pre-authorized retraining |
| EU | MDR Class IIa+ conformity, EU AI Act high-risk compliance |
| Post-market | Surveillance, monitoring plan per PCCP, annual reporting |
| Cybersecurity | SBOM, pen-test per FDA 2023 final guidance |

## Key Principles

1. **Truthful labeling** — The regulatory state of the product is never ambiguous. DDE is currently a research tool; nothing in the product, documentation, or communications implies otherwise.
2. **Evidence-first** — No regulatory claim is made without supporting documentation. No clearance is asserted without an authorization letter.
3. **Audit-ready by default** — All model releases, dataset changes, and QMS modifications produce immutable records from day one.
4. **PCCP-forward design** — Future adaptive retraining is planned now so the submission pathway is not blocked by architectural decisions.
5. **Dual-track readiness** — US (FDA) and EU (MDR/AI Act) strategies run in parallel from the validation phase onward.

## Interfaces

| Interface | Direction | Purpose |
|---|---|---|
| AI Research | Inbound | Model specs, evaluation results for regulatory classification |
| Platform Eng | Inbound/Outbound | UI disclaimer placement, audit trail implementation |
| Regulated AI | Inbound | Validation gate results, provenance records |
| Business | Outbound | Regulatory posture for partnerships, investor materials |
| Leadership | Outbound | Regulatory risk, timeline, submission readiness |

_Last updated: 2026-09-06_
