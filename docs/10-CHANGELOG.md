# 10-CHANGELOG — Therapeutic-AI

All notable changes. Format: dated entries per completed feature/phase.

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