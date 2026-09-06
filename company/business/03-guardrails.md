# Business / GTM / Operations — Guardrails

Operating rules for anything this department writes, says, or plans. These are binding; violations are raised to the COO.

---

## 1. No revenue claims without evidence

- Revenue is only "revenue" when money has been received and recorded in the financial runbook (`business-4`).
- Projections, pipeline value, and forecasted milestones are always labeled as projections — never stated as revenue, bookings, or "in revenue run-rate."
- Any revenue-like number in a doc must cite its source record (file + date) or carry an explicit "projection, unaudited" qualifier.
- The staged revenue model in `00-charter.md` describes intent; it is not a financial statement.

## 2. No scope creep that splits the single-product focus

- Every business initiative must attach to a concrete slice of the Drug Discovery Engine (`product/drug-discovery-engine/`).
- New market, pricing, or partnership ideas that do not serve the DDE are documented and deferred — they do not become projects.
- The Partnerships Agent maps every pipeline entry to a DDE capability; an unmappable entry is parked, not worked.
- If a proposed opportunity would fund work outside the DDE, it escalates to the COO before any commitment, per the single-product rule in `00-OPERATING-MODEL.md`.

## 3. Research-use-only disclaimer in all external marketing

- Every external-facing message (marketing copy, pitch deck, outreach email, case study, landing page, demo) must carry:

  > "Drug Discovery Engine is an AI research platform for drug-discovery research only. It is not a medical device and is not for clinical or patient decision-making."

- No copy may imply clinical readiness, FDA clearance, or therapeutic efficacy. Reference `regulated-ai/` and `regulatory/` before any claim touching clinical use.
- The disclaimer is verified in review before anything goes out; a missing disclaimer means the piece does not ship.

## 4. No fabricating customer traction

- Never invent customers, usage numbers, quotes, testimonials, or "design partners."
- Any named customer, lab, or partner must have a real intake record (source, date, contact) in the partnership pipeline or early-adopter log.
- Anonymized/representative usage figures must be explicitly labeled as illustrative examples, sourced from internal DDE runs — never presented as customer data.
- Synthetic screenshots, mock usage charts, and pricing mock concepts are labeled "concept / illustrative" wherever displayed.

---

## Enforcement

- All four rules are checked at the review gate of `business-1` before any external output.
- The Operations/Finance Agent logs guardrail exceptions in the monthly review; repeat violations escalate to the COO.
- `regulatory/` and `regulated-ai/` sign off on anything crossing into clinical, SaMD, or validation claims before external distribution.

---
_Last updated: 2026-09-06_