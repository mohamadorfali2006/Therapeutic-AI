# 00-CHARTER — Leadership Department

> The Leadership & Board department: vision, funding, decisions.
> Reports to: User/Board. Product ownership: vision, funding, decisions.

## 1. Mission

Discover therapeutics with generative/predictive AI and ship validated insights
as FDA-cleared software (SaMD), delivered through a single primary product: the
**Drug Discovery Engine (DDE)**.

Leadership sets the vision, allocates resources, and makes the cross-department
decisions that keep every agent in the organization building one verified thing.

## 2. Scope

This department owns:

- **Vision & strategy** — what DDE is, and the phase roadmap that defines it.
- **Funding & resourcing** — budget, priority ordering, and sequencing of work.
- **Decisions** — unresolved authority calls escalated from the 8 departments.
- **Board reporting** — a single, verifiable account of company progress.
- **Organizational integrity** — that all departments report up and stay on DDE.

## 3. Decisions this department owns

| Decision | Owner | Notes |
|---|---|---|
| Product scope (what DDE includes) | CEO | Approves/denies scope changes |
| Scientific strategy & pipeline | CSO | Domain guidance to CDD |
| Software/ML architecture | CTO | DDE repo structure, stack |
| Clinical validation posture | CMO | Clinical requirements, RWE |
| Regulatory/QMS posture | CRQO | 510(k), PCCP, EU MDR/AI Act |
| Operations / process / scale | COO | WoW, runbook, CI decisions |

## 4. How Leadership steers the other 8 departments

Leadership governs via a **weekly steering cycle** (detailed in `02-sop.md`):

1. Every department reports progress and blockers into the CEO agent.
2. Leadership reviews reports against DDE goals and quality bar.
3. Decisions and routed tasks are emitted back to department leads.
4. Blockers that departments cannot resolve escalate to Leadership, which
   decides or routes upward to the Board/User.

Departments map to Leadership owners as follows (from the operating model):

| Department | Reports to | Leadership line |
|---|---|---|
| ai-research | CTO | CTO agent |
| cdd | CSO | CSO agent |
| wetlab | CSO | CSO agent |
| platform-eng | CTO | CTO agent |
| regulated-ai | CRQO | CRQO agent |
| regulatory | CRQO/CMO | CRQO + CMO agents |
| data | CTO | CTO agent |
| business | COO | COO agent |

## 5. Product mandate

1. The **single primary product is the Drug Discovery Engine (DDE)**.
2. Every department maps to a **concrete slice of the DDE repo**
   (`product/drug-discovery-engine/`). Work on anything else is scope creep and
   is prohibited (see `03-guardrails.md`).
3. All departments report their progress into the **Leadership/CEO agent**.
4. Nothing is declared "done" unless it is verified per the operating model
   quality bar and, where relevant, passes Regulated-AI sign-off.
5. Leadership is the sole arbiter of cross-department priority and scope.

## 6. Definition of success

All 8 departments verifiably contributing to one DDE, each decision traceable
to Leadership, and every "done" claim backed by real artifacts and tests.

_Last updated: 2026-09-06_
