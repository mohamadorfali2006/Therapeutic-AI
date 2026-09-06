# Wet Lab / Biology — Guardrails

**Department:** `wetlab/`
**Purpose:** Non-negotiable rules governing validation claims, experimental honesty, and feedback integrity.
**Owner:** wetlab-1 (Head of Biology Agent)
**Review cadence:** Quarterly, or upon any regulatory/ML pipeline change.

---

## 1. Claims Must Be Honest

**Rule:** Every validation-claim record must accurately represent its measurement status. In the foundation phase, no claim has been physically measured. All claims are virtual.

- A claim with `status: proposed`, `in_design`, or `ready_for_test` is explicitly **not measured**.
- A claim with `status: measured` must carry a `measurement_type` field that is either `physical` (real lab data) or `simulated` (literature/historical inference). There is no third option.
- Never use ambiguous language that implies physical measurement when only a simulation exists.
- Marketing, external communications, and regulatory filings must not cite simulated claims as experimental confirmations.

**Consequence of violation:** Any claim found to misrepresent its measurement status is flagged, terminal-statused as `archived`, and reported to CSO. The originating agent is reviewed for correction.

---

## 2. No Fabricated Experimental Results

**Rule:** No agent may generate, fabricate, or fabricate-adjacent synthetic data and present it as experimental measurement.

Prohibited:
- Creating fake assay results and marking `measurement_type: physical`.
- Inventing numeric values not sourced from literature, historical data, or actual experiments.
- Copying another claim's measured result and applying it to a different prediction without documentation.
- Altering measured values to fit within an acceptance window.

Required:
- Every `simulated_result` must cite its source (literature reference, historical dataset, or reasoning basis).
- Every future `physical` measurement must trace to a specific assay protocol, instrument, and operator (or lab automation record).

---

## 3. Feedback Loop Must Reference Exact model_version

**Rule:** Every feedback record sent to the ML retraining pipeline must include the exact `model_version` string from the originating claim. No exceptions.

- Feedback records with a blank, generic, or "latest" `model_version` are rejected by the ML pipeline ingestion gate.
- If a claim spans multiple model versions (e.g., prediction made on v1.2, retrained on v2.0, re-predicted), each prediction produces a separate claim or a new versioned entry on the same claim. The feedback always references the version that made the specific prediction being validated.
- The ML pipeline logs every feedback receipt with `claim_id` + `model_version` for auditability.

**Consequence of violation:** Feedback records with incorrect or missing `model_version` are quarantined and reported to wetlab-1 and AI Research for correction before retraining proceeds.

---

## 4. Claim Lifecycle Integrity

**Rule:** Every claim must reach a terminal status. No open-ended claims.

- Terminal statuses: `confirmed`, `discontinued`, `archived`, `superseded`.
- Claims stuck in non-terminal status for > 30 days without documented justification are auto-flagged in the monthly registry audit.
- Claims may not be deleted from the registry. Only terminal-statused and annotated.

---

## 5. Traceability

**Rule:** Every artifact in the validation workflow must be traceable to its source.

| Artifact | Must trace to |
|---|---|
| Validation-claim record | Specific DDE prediction (model_version + prediction ID) |
| Assay design document | Claim ID + biological rationale source |
| Feasibility report | Target protein ID + literature or database reference |
| QC criteria | Assay design document + ML pipeline ingestion spec |
| Feedback record | Claim ID + model_version + measured/simulated value source |
| Registry changes | Git commit with author and timestamp |

---

## 6. Separation of Virtual and Physical

**Rule:** Until a physical wet lab is operational, maintain clear separation between virtual and physical validation in all documentation, registry records, and communications.

- Virtual claims use `measurement_type: simulated` and are explicitly labeled as such in any summary report.
- Physical claims use `measurement_type: physical` and require an attached assay execution record.
- Transitioning from virtual to physical requires: (a) a physical lab to be declared operational by CSO, (b) wetlab-1 approval, and (c) an update to this guardrails document.

---

## 7. Department-Level Review Gate

**Rule:** No validation-claim record is published to the ML pipeline or external stakeholders without wetlab-1 review and approval.

- Claims touching regulated-model predictions additionally require Regulated-AI co-sign.
- Assay designs additionally require wetlab-2 self-review and wetlab-1 approval.
- QC criteria additionally require AI Research confirmation of data format compatibility.

---

## 8. Audit and Compliance

| Activity | Frequency | Owner |
|---|---|---|
| Registry audit (stale claims, schema compliance) | Monthly | wetlab-1 |
| Guardrails review | Quarterly | wetlab-1 + CSO |
| Feedback loop integrity check (model_version accuracy) | Per retraining cycle | wetlab-1 + AI Research |
| Simulated result source audit | Quarterly | wetlab-1 |
| Full validation workflow retrospective | Annually | CSO + all wetlab agents |

---

*Guardrails — Therapeutic-AI Wet Lab / Biology*
*Last updated: 2026-09-06*
