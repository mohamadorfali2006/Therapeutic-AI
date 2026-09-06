# 02-SOP — Weekly Review Cycle & Decision Procedure

Standard operating procedure for how Leadership governs all 8 departments.
Run this on a fixed cadence (weekly minimum; ad-hoc as blockers appear).

## 1. Cycle: goal → reports → decisions → routed tasks

| Step | Who | What happens |
|---|---|---|
| 1. Restate goal | CEO | Re-state the DDE goal and success criteria for the cycle. |
| 2. Collect reports | All depts | Each department posts progress/blockers into the CEO agent (per product mandate). |
| 3. Review | Leadership | Each executive reviews reports against the goal and quality bar. |
| 4. Decide | Leadership | Record decisions on scope, priority, blocked work. |
| 5. Route tasks | Leadership | Emit routed tasks back to department leads with clear owners and gates. |
| 6. Verify & log | COO | Confirm routed tasks land; update HANDOFF.md and company docs. |

**Inputs for step 2** — each report must contain, at minimum:
- What was delivered (concrete artifacts, not summaries)
- Verification status (build/lint/tests per Verify Commands)
- Blockers and any escalation requests

## 2. How Leadership approves plans before execution

1. Department claims a piece of DDE work and posts a **plan** (goal, steps,
   tech choices, verification approach).
2. The owning Leadership agent reviews the plan against the DDE scope and the
   quality bar.
3. **Scope check:** if the work goes beyond DDE, it is rejected (see guardrails).
4. **Regulatory check:** if the plan touches model/validation logic, route it to
   the CRQO agent for Regulated-AI sign-off **before** execution begins.
5. Leadership records the approved plan (owner, acceptance criteria, gate). The
   department then executes end-to-end without further per-step approval.
6. Approval is a single gate, not a per-change wait: one approved plan
   authorizes the full execution of that plan.

## 3. How Leadership escalates blockers

- A department that cannot self-resolve raises to its department lead, then to
  its Leadership owner.
- Leadership owners triage the blocker:
  - **Decidable now** → Leadership decides and routes the resolution task.
  - **Cross-department** → COO routes/coordinates; CEO arbitrates if owners clash.
  - **Scope or policy** → CEO + CRQO (regulatory) escalate to Board/User.
  - **Irreversible action** → pause and require Board/User approval (guardrails).
- Every escalation is logged with owner, due date, and resolution; unresolved
  blockers are reviewed at the start of the next cycle.

## 4. Cadence & artifacts

| Cadence | Activity | Artifact |
|---|---|---|
| Weekly | Full steering cycle | Cycle review + routed task log |
| Ad-hoc | Blocker resolution | Escalation record |
| Per-ready-work | Plan approval | Approved plan record |
| End of cycle | State update | HANDOFF.md + company docs |

## 5. Exit criteria for a cycle

- Every department report reviewed and acknowledged.
- All decisions recorded with owners and gates.
- No unresolved blocker left silent (escalated or closed).
- HANDOFF.md updated; Obsidian mirror synced.

_Last updated: 2026-09-06_
