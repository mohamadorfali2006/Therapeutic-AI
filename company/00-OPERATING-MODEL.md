# 00-OPERATING-MODEL — Therapeutic-AI Agent Company Constitution

> How the company runs as an autonomous agent-based organization.
> This is the master document. Every department (`company/<dept>/`) abides by it.

## 1. Mission
Discover therapeutics with generative/predictive AI and ship validated insights as FDA-cleared software (SaMD). The **single primary product** is the **Drug Discovery Engine (DDE)** — a research platform for target→candidate acceleration, with regulated-AI validation built in.

## 2. Structure: agent-based departments
The company is staffed by **specialist AI agents**, grouped into departments mapped 1:1 to the org design (`org/roles/` and `org/README.md`).

| Dept dir | Department | Reports to | Product ownership |
|---|---|---|---|
| `leadership/` | Leadership & Board | User/Board | Vision, funding, decisions |
| `ai-research/` | AI Research & ML | CTO | ML models, evaluation |
| `cdd/` | Computational Drug Discovery | CSO | Target/model domain guidance |
| `wetlab/` | Wet Lab / Biology | CSO | Experimental validation (virtual) |
| `platform-eng/` | Software & Platform Engineering | CTO | DDE backend + web |
| `regulated-ai/` | Regulated AI / ML-Validation | CRQO | Validation gates, provenance |
| `regulatory/` | Regulatory, Quality & Clinical | CRQO/CMO | FDA/QMS posture |
| `data/` | Data & Infrastructure | CTO | Datasets, provenance, infra |
| `business/` | Business / GTM / Ops | COO | Product strategy, partnerships |

## 3. How agents work
Each department defines its roster in `01-agents.md` using this schema:

```yaml
agent:
  id: <dept>-<n>
  name: <Role Agent>
  mission: <one phrase>
  skills: [list of capabilities]
  tools: [repo paths, scripts, MCPs]
  inputs: [what it consumes]
  outputs: [artifacts it produces: files, reports, decisions]
  autonomy: watch / act / decide   # watch=report, act=implement, decide=authoritative
  kpis: [measurable outcomes]
  review_gate: <how output is verified before merging>
```

**Operating rules:**
1. **Outputs over summaries** — agents return real artifacts (files, tests, reports), not prose.
2. **Skills = SOPs** — repeatable work uses the department's `02-sop.md` procedures.
3. **Review gates** — every artifact passes the department's quality gate (tests, lint, spec check) before integration. Regulated-AI signs off on anything touching model/validation logic.
4. **Escalation** — an agent that cannot self-resolve raises to its department lead; leaders raise to Leadership/CEO agent.
5. **GMP-grade traceability** — anything touching models/data/regulatory must be reproducible and provable (provenance everywhere).
6. **Git discipline** — every working change commits with a conventional message; GitHub backup per global rules.

## 4. Product: Drug Discovery Engine (DDE) — what we're building
A working research platform foundation:
- **Backend API** (FastAPI): model registry, prediction, validation gate, provenance/traces.
- **ML service**: baseline property predictor (pure-Python fingerprints + sklearn regressor), training + evaluation pipeline.
- **Validation spine**: regression gates + evaluation reports (the regulated-AI function, in code).
- **Web dashboard**: model monitoring + prediction console (foundation).
- **Infra**: Dockerfile, CI workflow, run book.

Non-goals for this foundation: production FDA submission, RDKit dependency, real wet-lab, external compute. These are future phases; the foundation is built so they slot in.

## 5. Quality bar (all departments)
- Build/lint/tests pass before "done" (Verify Commands).
- No secrets in code. No fake-green reporting.
- Every phase ends with: End-of-Task report, git commit, Obsidian sync, HANDOFF update.

## 6. Single product, all departments
Every department's `01-agents.md` maps its agents to a **concrete slice of the DDE repo** (under `product/drug-discovery-engine/`) so the org is verifiably building one thing.

_Last updated: 2026-09-06_