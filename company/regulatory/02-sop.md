# Regulatory, Quality & Clinical — Standard Operating Procedures

## SOP-RC-01: Feature Classification (Research vs. Device)

Every new feature or capability added to DDE must be classified before merge. Use this checklist.

### Decision Checklist

| # | Question | If YES | If NO |
|---|---|---|---|
| 1 | Does the feature provide information intended to be used for diagnosis, treatment, or prevention of disease? | Classify as **Device**. Stop here. Trigger SaMD pathway. | Continue to Q2. |
| 2 | Does the feature output influence or replace a clinical decision made by a healthcare professional? | Classify as **Device**. Stop here. | Continue to Q3. |
| 3 | Is the feature output intended for use by a patient or clinician in a point-of-care setting? | Classify as **Device**. Stop here. | Continue to Q4. |
| 4 | Is the feature used exclusively by Therapeutic-AI researchers for internal R&D on non-human data? | Classify as **Research**. Document and proceed. | Continue to Q5. |
| 5 | Is the feature output clearly labeled as preliminary, non-validated, and not for clinical use? | Classify as **Research** with mandatory disclaimer. | **Escalate to CRQO.** Do not merge until classified. |

### Process

1. Author of the feature completes the checklist above in the PR description.
2. `regulatory-3` (QA Agent) reviews the classification in the PR review gate.
3. If classified as **Device**: PR is blocked. US Regulatory Agent (`regulatory-1`) initiates submission pathway assessment.
4. If classified as **Research**: PR proceeds with disclaimer requirement verified.
5. Classification decision is recorded in the QMS change-control log.

### Output Artifact

- Classification record in the change-control log, referencing the PR, checklist answers, and reviewer.

---

## SOP-RC-02: Mandatory Disclaimer Placement in Product UI

### Requirement

The DDE web dashboard must display the following disclaimer string on every page:

```
For research use only. Not a medical device.
```

### Placement Rules

| Rule | Detail |
|---|---|
| Visibility | Always visible. Not hidden behind menus, tooltips, or expandable sections. |
| Location | Footer of every page, minimum. Additionally in page header or sidebar on dashboard and prediction views. |
| Persistence | Cannot be dismissed, hidden, or removed by end users. |
| Styling | Readable font (minimum 12px), sufficient contrast ratio (WCAG AA), distinct from interactive elements. |
| Localization | English is primary. If UI supports additional languages, disclaimer must be translated and present in all supported languages. |

### Verification

1. Platform Eng includes disclaimer in the shared layout component so all routes inherit it automatically.
2. QA Agent (`regulatory-3`) verifies disclaimer presence on every route during UI review (Playwright-based clickability audit per `09-TESTING.md`).
3. Any UI change that could affect disclaimer visibility requires QA sign-off before merge.

### Technical Reference

The disclaimer string is defined in `product/drug-discovery-engine/` configuration and referenced by `regulatory-status.json`:

```json
{
  "disclaimer_required": true,
  "disclaimer_text": "For research use only. Not a medical device."
}
```

---

## SOP-RC-03: QMS Change-Control Minimums

Every change to any repository under `product/drug-discovery-engine/` requires a QMS change-control record. This applies from day one, even while the product is in research-only status.

### Minimum Record Contents

| Field | Required | Description |
|---|---|---|
| Change ID | Yes | Unique identifier (e.g., `CC-2026-00001`) |
| PR / Commit Reference | Yes | Link to the pull request or commit hash |
| Date | Yes | Date the change was merged |
| Author | Yes | Agent or human who authored the change |
| Reviewer | Yes | Agent or human who reviewed and approved |
| Change Description | Yes | Plain-English summary of what changed |
| Classification Impact | Yes | Did the change affect the research/device classification? (Y/N + details) |
| Regulatory Impact | Yes | Does the change affect any regulatory submission or QMS record? (Y/N + details) |
| Test Evidence | Yes | Reference to test results (build, lint, test output) |
| Approval | Yes | CRQO approval for changes touching regulatory, validation, or model logic |

### Process

1. Every PR includes a change-control section in its description.
2. On merge, `regulatory-3` (QA Agent) creates or validates the change-control record.
3. Records are stored append-only (see `03-guardrails.md`).
4. Monthly audit: QA Agent reviews all change-control records for completeness.

---

## SOP-RC-04: Audit Trail for Model Releases

Every model release (training run, evaluation, promotion, or retirement) produces an immutable audit record.

### Required Audit Record Fields

| Field | Description |
|---|---|
| Model ID | Unique model identifier |
| Version | Semantic version or commit-linked version |
| Release Date | Timestamp of release |
| Author | Agent or human who initiated the release |
| Training Data | Dataset identifiers, versions, checksums, split registry references |
| Evaluation Results | Metrics on locked test split, calibration data, OOD detection results |
| Regression Analysis | Comparison to previous model version (if applicable) |
| Classification Check | Result of SOP-RC-01 checklist for this model's intended use |
| Approval | CRQO sign-off for models entering any validation or submission pathway |
| PCCP Reference | If applicable, which PCCP modification protocol this release follows |

### Process

1. `regulated-ai` generates the audit record as part of the model promotion pipeline.
2. `regulatory-3` (QA Agent) validates completeness before the model is marked as released.
3. Records are append-only and version-controlled. No record may be edited after finalization; corrections require a new record referencing the original.

---

_Last updated: 2026-09-06_
