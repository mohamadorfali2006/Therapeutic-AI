# 01-IMPLEMENTATION-PLAN — Therapeutic-AI

## Mission
Accelerate drug discovery with generative/predictive AI **and** ship validated insights to clinicians as FDA-cleared software (SaMD).

## Dual product lines
1. **Drug Discovery Engine** — AI + wet-lab validation for target → candidate.
2. **SaMD Clinical Products** — FDA-cleared software operationalizing validated insights at the point of care.

## Guiding strategy
- 510(k)/De Novo is the primary FDA path (~90% of AI devices clear via 510(k)).
- **PCCP-first**: build adaptive-AI validation infrastructure from day one so retraining is pre-authorized.
- **Regulated-AI team reports to Regulatory/Quality** (independent of shipping pressure).
- **In-house wet lab** closes the design→build→test→learn loop.
- EU MDR + EU AI Act compliance runs in parallel with FDA.

## Target org: 84 roles across 9 functions

| # | Function | Headcount |
|---|---|---|
| 1 | Executive Leadership | 6 |
| 2 | AI Research & ML | 14 |
| 3 | Computational Drug Discovery | 10 |
| 4 | Wet Lab / Biology | 8 |
| 5 | Software & Platform Engineering | 14 |
| 6 | Regulated AI / ML-Validation | 8 |
| 7 | Regulatory, Quality & Clinical | 10 |
| 8 | Data & Infrastructure | 6 |
| 9 | Business / GTM / Ops | 8 |
| **Total** | | **84** |

## Phases

### Phase 1 — Leadership & Foundation (Months 0–3)
**Goal:** Stand up executive team + core platform/data/regulatory leads; start SaMD clock immediately.
**Hires (~10):** CEO, CSO, CTO, CMO, CRQO, COO, Head of Engineering, VP AI Research, Head of Data, Head of Regulatory Affairs (US).
**Deliverables:**
- FDA Q-Submission strategy + predicate mining.
- ISO 13485 QMS skeleton + IEC 62304 design-control framework.
- Define data governance (provenance, training/test separation) principles.
- `docs/05-DATABASE.md` + `docs/02-ARCHITECTURE.md` v1.

### Phase 2 — Core Platform + Regulated-AI Spine (Months 3–9)
**Goal:** Build the platform and — critically — the PCCP operational validation pipeline.
**Hires (~25):** Platform Eng, ML-Validation team (first!), QA/QMS, RA (US + EU in parallel), Security Engineer, Data Engineers.
**Deliverables:**
- CI/CD-backed validation pipeline (regression gates on every change).
- Data catalog + lineage system live.
- Initial model training/inference infra (GPU cluster spec).
- Predicate + PCCP scope drafted; Q-Submission filed.

### Phase 3 — Science Expansion (Months 9–18)
**Goal:** Stand up full research + wet-lab capacity; begin clinical validation planning.
**Hires (~20):** Computational Drug Discovery, Wet Lab, ML Scientists, Clinical Affairs.
**Deliverables:**
- Design→build→test→learn closed loop operating.
- First candidate programs active; model evaluation/calibration framework live.
- Validation study protocol drafted (for 510(k)/De Novo evidence).

### Phase 4 — Scale / GTM (Months 18–24+)
**Goal:** Scale to ~84, launch GTM, submit/clear, post-market.
**Hires (~15):** Head of BD, BD Managers, General Counsel, Finance, People, clinical + RA expansion.
**Deliverables:**
- First SaMD submission(s) filed; EU MDR conformance progressing.
- Post-market surveillance plan live (PCCP-consistent).
- Commercial partnerships signed.

## Status tracking
- [x] Phase 0 — Company infrastructure + DDE product foundation (2026-09-06): 9 agent-staffed departments in `company/`; working Drug Discovery Engine MVP (FastAPI + Pure-Python ML baseline + validation gate + web dashboard) with 10 passing tests, live-verified on localhost:8011.
- [ ] Phase 1 — Leadership & Foundation (pending hiring/staffing)
- [ ] Phase 2 — Core Platform + Regulated-AI Spine (pending)
- [ ] Phase 3 — Science Expansion (pending)
- [ ] Phase 4 — Scale / GTM (pending)

_Dates filled in as phases begin._