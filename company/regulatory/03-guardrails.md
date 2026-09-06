# Regulatory, Quality & Clinical — Guardrails

These rules are non-negotiable. Violations halt work until resolved. No agent may override them without explicit CRQO and Leadership authorization.

---

## Guardrail 1: Never Claim Regulatory Clearance Without Evidence

### Rule

No document, UI element, marketing material, partnership communication, or internal report may state or imply that the DDE or any Therapeutic-AI product has received FDA clearance, CE marking, or any regulatory authorization unless:

1. A signed authorization letter (510(k) clearance, De Novo designation, CE certificate) is on file.
2. The specific product version and intended use covered by the authorization are identified.
3. CRQO has approved the claim for accuracy.

### Enforcement

- All external-facing materials go through `regulatory-1` (US) or `regulatory-2` (EU) review.
- Internal dashboards display `regulatory-status.json` as the single source of truth.
- Any reference to regulatory status that contradicts `regulatory-status.json` is a violation.

### Current State

DDE has **not** received any regulatory clearance. Current status: `research_only`. No language in any context may suggest otherwise.

---

## Guardrail 2: Research-Only Labeling Must Appear

### Rule

The disclaimer `"For research use only. Not a medical device."` must be visible:

- On every page of the DDE web dashboard (per SOP-RC-02).
- In every generated report or output document that leaves the platform.
- In README and documentation files that describe the product's current capabilities.
- In any demo, presentation, or walkthrough of the current product.

### Enforcement

- `regulatory-3` (QA Agent) includes disclaimer verification in every UI review gate.
- CI checks verify the disclaimer string is present in the shared layout component.
- Removing or hiding the disclaimer is a blocking change that requires CRQO approval and cannot be merged.

### Exception

When DDE receives FDA clearance for a specific SaMD component, that component's UI may replace the disclaimer with the appropriate cleared-device labeling. The research-use disclaimer remains on all non-cleared features.

---

## Guardrail 3: No Medical Claims on DDE Research Output

### Rule

DDE outputs (predictions, compound rankings, target assessments, validation metrics) are research artifacts. They must never be presented, framed, or interpreted as:

- Diagnostic conclusions
- Treatment recommendations
- Clinical decision support
- Evidence of efficacy, safety, or therapeutic value
- substitutes for clinical trials or peer-reviewed validation

### Allowed Framing

- "Computational prediction — for research use only"
- "Preliminary assessment — not validated for clinical use"
- "Research output — requires independent experimental validation"

### Enforcement

- Output templates in the DDE include mandatory research-only framing language.
- `regulatory-1` reviews any feature that generates outward-facing output.
- Business and partnership materials referencing DDE outputs must include research-only context.

---

## Guardrail 4: QMS Records Are Immutable and Append-Only

### Rule

All QMS records — change-control entries, CAPA records, audit trail entries, model release audit records, classification decisions — are append-only. Once written and finalized:

1. **No record may be modified or deleted.**
2. **Corrections** are made by creating a new record that references the original and states the correction.
3. **The original record remains readable** and is never superseded or hidden.
4. **Version control** (git) enforces immutability at the repository level.

### Storage

| Record Type | Location | Format |
|---|---|---|
| Change-control records | QMS log (append-only) | Structured entries in designated QMS file |
| CAPA records | CAPA log (append-only) | Structured entries with status tracking |
| Model release audit | Model registry audit trail | JSON/structured records per model version |
| Classification decisions | Change-control record | Linked to the relevant PR or feature |
| `regulatory-status.json` | Product root | Updated only by authorized agents; git history is the audit trail |

### Enforcement

- QMS logs are stored in a location where write operations only append; no edit/delete tooling is available for finalized records.
- `regulatory-3` (QA Agent) runs a monthly integrity check: verify no QMS record has been altered or removed from the append-only log.
- Any detected modification or deletion of a QMS record is a critical CAPA trigger.

---

## Guardrail 5: PCCP Discipline for Future Adaptive AI

### Rule

When DDE transitions to SaMD, any adaptive retraining, model update, or algorithm modification must follow the Predetermined Change Control Plan (PCCP) that was authorized in the regulatory submission. Specifically:

1. No model update to a cleared SaMD component occurs outside the PCCP modification protocol.
2. Each update produces a PCCP evidence record linking the change to the authorized protocol.
3. `regulatory-1` (US Agent) and `regulatory-3` (QA Agent) jointly verify PCCP compliance before any model promotion.

### Current Applicability

This guardrail is **dormant** while DDE is in research-only status. It becomes active when a SaMD submission is filed. However, the PCCP-first design principle applies now: model pipelines are built so that future PCCP constraints can be enforced without re-architecture.

---

## Violation Response

| Severity | Example | Response |
|---|---|---|
| Critical | Claiming FDA clearance without authorization letter | Immediate halt. CAPA initiated. Leadership notified. |
| Critical | Removing disclaimer from UI without CRQO approval | Immediate halt. CAPA initiated. Change reverted. |
| High | Medical claim in product output or materials | Halt affected feature. CAPA initiated. Review by regulatory-1. |
| High | QMS record modification or deletion | CAPA initiated. Integrity audit triggered. |
| Medium | Missing change-control record for a repo change | Record created retroactively. Process gap CAPA if pattern detected. |
| Medium | Incomplete model release audit record | Hold model promotion until record is complete. |

---

_Last updated: 2026-09-06_
