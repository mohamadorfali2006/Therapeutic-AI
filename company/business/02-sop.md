# Business / GTM / Operations — Standard Operating Procedures

---

## SOP-A: Monthly Product-Milestone Review

**Purpose:** Turn DDE progress into refreshed product priorities, so business activity always tracks the single product.

### Cadence and owner
- Monthly, run by the Operations / Finance Agent, chaired by Head of Business Development.
- Input gathered from every department's milestone report (platform-eng, ai-research, regulated-ai, data).

### Steps

| Step | Action | Artifact |
|---|---|---|
| 1 | Collect milestone status from all departments | Milestone notes |
| 2 | Compare completed milestones against the roadmap (`docs/01-IMPLEMENTATION-PLAN.md`) | Gap list |
| 3 | Map gaps to business impact (demo readiness, feature asks, positioning) | Impact notes |
| 4 | Decide top 3 product priorities for the next month | Priority list |
| 5 | Publish priorities alongside the decision rationale | `business/monthly-review-YYYY-MM.md` |
| 6 | Deliver confirmed priorities to product/ and platform-eng as backlog input | Routed request |

### Output contract
- Priorities are concrete and DDE-scoped — no priority may reference work outside the DDE.
- Each priority names the owning department and its acceptance criterion.
- Review minutes are committed to `company/business/monthly-review-YYYY-MM.md` within 3 working days.

---

## SOP-B: Early-Adopter Feedback Loop

**Purpose:** Collect, triage, and route feedback from design partners so it improves the DDE and never sits in an inbox.

### Pipeline: Collect -> Triage -> Route -> Confirm

| Stage | Owner | Action | TAT |
|---|---|---|---|
| Collect | Partnerships Agent | Log feedback (source, date, contact, verbatim, DDE feature touched) | On receipt |
| Triage | Product Strategy Agent | Classify: product / ML / regulatory / business; dedupe; tag severity | 3 working days |
| Route | Operations/Finance Agent | Assign to owning department with a ticket entry | 5 working days from intake |
| Confirm | Business lead | Notify the partner that feedback was received and where it went | With routing |

### Classification tags
- `product` — UX, dashboard, prediction console -> platform-eng frontend/backend
- `ml` — model behavior, evaluation, validity -> ai-research + regulated-ai sign-off
- `regulatory` — anything clinical-adjacent -> regulatory (never routed elsewhere)
- `business` — pricing, positioning, partnership -> product strategy / business lead

### Rules
- Every item has a single owning department. No shared-owner items.
- Regulatory-classified items bypass normal priority and go to regulatory first.
- Unroutable items are returned to Product Strategy Agent with a reason, never silently dropped.

---

## SOP-C: Cost / Runway Review (Research Stage)

**Purpose:** Keep a research-stage company honest about money: track committed and projected spend, and report runway with evidence, monthly.

### Runway definition
Runway = cash available / trailing 90-day burn. Burn is the average of recorded expenses over the trailing 90 days — estimates are labeled as projections, never presented as actuals.

### Monthly review steps

| Step | Action | Notes |
|---|---|---|
| 1 | Record all committed cost lines (compute, tools, staff, pilot credits) | From recorded figures only |
| 2 | Compute trailing 90-day burn and runway | State the numbers and the period |
| 3 | List upcoming commitments and one-off spend | Flag anything over a committed threshold |
| 4 | Assess server/CI/lab costs against DDE milestone needs | Aligns spend with product progress |
| 5 | Produce the monthly cost/runway record | `business/runway-YYYY-MM.md` |

### Rules
- No revenue is booked before money is received and recorded. Revenue projections live in the charter's staged model, never in financial records.
- Any commitment above a department-defined threshold requires Head of Business Development sign-off; larger commitments escalate to Leadership.
- If runway falls below 6 months, an escalation is raised immediately — the monthly cadence does not wait.

---
_Last updated: 2026-09-06_