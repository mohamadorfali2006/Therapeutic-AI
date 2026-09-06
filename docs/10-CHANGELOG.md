# 10-CHANGELOG — Therapeutic-AI

All notable changes. Format: dated entries per completed feature/phase.

## 2026-09-06 — Sprint S1 closed: DDE v0.2 (company platform runs live)
- **Company runtime added:** `company/platform/run.py` (CLI state machine: plan sprints, dispatch tasks by department, record Regulated-AI gates, status board, sprint report). Persistent state in `company/platform/state.json`.
- **Sprint S1 executed:** 7 tasks, 5 departments, all gated PASS, closed 7/7. Report: `company/platform/sprint-S1-report.md`.
- **Product v0.2.0 (DDE):**
  - 2nd demo property **logS** (aqueous solubility proxy) + property-routed API (`/api/v1/predict?property=logp|logS`), model registry `baseline-logp` / `baseline-logS`.
  - Dataset v2 `seed-2026.09.06-v2` (57 compounds, logS) with provenance doc.
  - ECFP-style hashed fingerprints (pure Python, radius 2, 256 bits) in `ml/fingerprints.py` — raised logP R2 0.658 → 0.722.
  - `/api/v1/validate` returns per-model gates (all at once or `?property=`, 503 on unknown property).
- **Verified:** 15/15 pytest; both validation gates PASS (logp R2=0.7222, logS R2=0.6079); live routes on 8011 all 200; Playwright QA **14/14** (incl. property dropdown routing + dual-theme).

## 2026-09-06 — Dashboard Visual QA passed
- **Added:** Playwright visual-QA suite (`product/drug-discovery-engine/tests/qa_dashboard.py`) + screenshots in `tests/qa-screenshots/`.
- **Verified:** 12/12 checks pass including theme toggle (dark `#0A0A0B` ↔ light `#F7F6F3`), predict flow renders value, trace fetch, invalid SMILES → 422. Screenshots saved for human review (model lacks image input).
- **Fixed:** theme-toggle test measured wrong element (now checks `html[data-theme]` + canvas bg).

## 2026-09-06 — Agent company + Drug Discovery Engine foundation
- **Added:** `company/` — 9 agent-staffed departments (leadership, ai-research, cdd, wetlab, platform-eng, regulated-ai, regulatory, data, business), each with charter, agent roster, SOPs, guardrails. Master `company/00-OPERATING-MODEL.md` constitution.
- **Added:** Drug Discovery Engine MVP (`product/drug-discovery-engine/`): FastAPI backend (model registry, prediction, validation gate, provenance/traces), pure-Python ML baseline (features → sklearn RandomForest, seed data, train/evaluate), append-only provenance store, static web dashboard, Dockerfile + docker-compose + CI.
- **Verified:** 10/10 tests pass; validation gate PASS (R2=0.6583 on locked test split); live routes verified 200 on localhost (health, models, predict, validate, traces, UI).
- **Note:** GitHub remote + push still pending user authentication (`gh` CLI not installed / no token).

## 2026-09-06 — Project scaffolding & org design
- **Added:** initial project skeleton (`docs/`, `org/`).
- **Added:** full documentation set (00-INDEX → 10-CHANGELOG).
- **Added:** org design — 84-role enterprise structure across 9 functions (docs in `org/roles/`).
- **Added:** phased implementation plan: Leadership (M0–3) → Core Platform + Regulated-AI Spine (M3–9) → Science Expansion (M9–18) → Scale/GTM (M18–24+).
- **Added:** architecture (Mermaid) with PCCP-first Regulated-AI validation pipeline.
- **Added:** AGENTS.md project rules; HANDOFF.md continuity file.
- **Note:** GitHub remote + push pending user authentication (`gh` CLI not installed / no token).

---

_Future entries appended per completed phase per `01-IMPLEMENTATION-PLAN.md`._