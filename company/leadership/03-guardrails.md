# 03-GUARDRAILS — Leadership Rules

Non-negotiable constraints on how Leadership and the organization operate.
These bind every department that reports into Leadership.

## 1. No scope creep beyond DDE

- The single primary product is the Drug Discovery Engine (DDE). Every
  department maps to a concrete slice of the DDE repo
  (`product/drug-discovery-engine/`).
- Any proposed work that does not serve DDE is **scope creep** and is rejected.
- New features must be justified as serving DDE's target→candidate
  acceleration with regulated-AI validation built in.
- Non-goals (production FDA submission, RDKit, real wet-lab, external compute)
  are future phases, not today's build. They may be planned, not shipped.
- If a department cannot map its deliverable to a DDE artifact, the work is
  parked until it can.

## 2. No unverified "done" claims

- "Done" means verified. Build/lint/tests pass per Verify Commands; artifacts
  exist and are provable.
- No fake-green reporting. A change that fails or wasn't run is never reported
  as passing.
- Every "done" claim must reference the real artifact (function, file, report)
  plus the verification evidence.
- Leadership rejects any "done" claim lacking verification, and returns it to
  the owning department with the gap stated.

## 3. No bypassing Regulated-AI sign-off

- Any change to **models or validation logic** requires CRQO / Regulated-AI
  sign-off **before** it is integrated or deployed.
- This covers the validation spine (regression gates, evaluation reports),
  model registry, prediction logic, and any PCCP/ML-Ops CI-CD that affects
  the regulated path.
- Research (non-SaMD) work remains fluid, but the moment work touches the
  validation/regulated spine it is gated.
- An agent that merges a model/validation change without sign-off has
  bypassed a mandatory gate and the change is reverted and re-reviewed.

## 4. Irreversible actions require board/user approval

Pause before taking any of the following; they require the Board/User:

| Irreversible action | Example |
|---|---|
| Deleting data | Dropping datasets, purging provenance logs |
| Spending money | Paid infrastructure, licenses, compute |
| Deploying to production | SaMD release, external public deployment |
| External communications | Customer-facing claims, regulatory submissions, press |
| Requiring credentials/auth | Manual sign-in, secrets, production access |

- Everything else: decide and proceed autonomously under the single approved
  plan gate (`02-sop.md`).
- An irreversible action taken without approval is treated as a guardrail
  breach: stop, record, escalate to Board/User, and roll back if possible.

## 5. Enforcement & consequence

- Guardrail breaches are logged in the escalation record and reviewed by the
  CEO agent at the next cycle.
- Repeated bypass of scope, verification, or sign-off gates triggers a
  process review by the COO agent and a Board/User report.
- No guardrail is overridden by convenience; any conflict escalates upward.

_Last updated: 2026-09-06_
