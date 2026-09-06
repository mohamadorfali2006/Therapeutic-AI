# HANDOFF — Therapeutic-AI

**Session date:** 2026-09-06 (updated at end of agent-company + product build)

## What was accomplished

### Round 1 — Scaffolding
- Scaffolded `C:/Users/PCD/Therapeutic-AI` with full org design (84 roles, 9 functions, `org/`) and documentation set (`docs/00-INDEX` → `10-CHANGELOG`).
- Initial git history: `d8460dd` scaffold, `e1921fd` handoff.

### Round 2 — Agent-based company + working product (this session)
- **Agent company (`company/`)**: 9 departments staffed with specialist AI agents — leadership, ai-research, cdd, wetlab, platform-eng, regulated-ai, regulatory, data, business. Each has `00-charter.md`, `01-agents.md` (YAML roster), `02-sop.md`, `03-guardrails.md`. Master constitution: `company/00-OPERATING-MODEL.md`.
- **Drug Discovery Engine (DDE) MVP** (`product/drug-discovery-engine/`) — the single primary product:
  - FastAPI backend (`app/main.py`): `/health`, `/api/v1/models`, `/api/v1/predict`, `/api/v1/validate`, `/api/v1/traces/{id}`, static dashboard `/`.
  - Pure-Python ML baseline (`ml/`): SMILES feature extraction (`features.py`), RandomForest regressor (`baseline.py`), seed dataset (`seed_data.py`), train/evaluate pipelines.
  - Append-only provenance store (`app/store.py`) — traceability for every prediction + validation.
  - Validation gate (owned by `company/regulated-ai`): `ml/evaluate.py` computes RMSE/MAE/R2 on locked test split; PASS at R2=0.6583.
  - Web dashboard (`web/index.html`) — dark/light theme, predict form, trace viewer, models table, health indicator, research-use-only badge.
  - Infra: `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml`, `.env.example`.

## Verification (real proof)
- `python -m pytest tests -q` → **10 passed** (auto-trains artifact via conftest fixture).
- Validation gate: `{"passed": true, "r2": 0.6583, "rmse": 0.8943, "mae": 0.5293, "n_test": 12}`.
- Live server verified (port **8011** — 8000 is occupied by another app, PID 41996):
  - `/health` → 200 `{"status":"ok","predictor_ready":true}`
  - `/api/v1/models` → 200, `/` UI → 200 (15,393 bytes)
  - `POST /api/v1/predict {"smiles":"CCO"}` → 200, prediction `logp=-0.0431`, trace_id, disclaimer
  - `POST /api/v1/validate` → 200, passed
  - `GET /api/v1/traces/trace-…` → 200 provenance record
- Obsidian mirror synced (62 files).

## Key decisions (made autonomously)
1. Single product = **Drug Discovery Engine research platform** (buildable foundation; SaMD later).
2. Pure-Python ML baseline (no RDKit dependency) — deterministic, reproducible.
3. Validation thresholds: R2 ≥ 0.50, MAE ≤ 20% of target range (per Regulated-AI SOP).
4. Provenance = append-only jsonl store; runtime data gitignored.
5. Port 8011 for local runs (8000 taken).

## Blocker / unresolved
- **GitHub remote + push NOT done.** `gh` CLI not installed; no `GH_TOKEN`.
  - Run: install `gh` (e.g. `winget install GitHub.cli`), `gh auth login`, then:
    - `gh repo create Therapeutic-AI --private --source=. --remote=origin --push`
  - Or set `GH_TOKEN` and I'll create + push the repo.
- Runtime provenance files (`app/data/*.jsonl`) are gitignored by design (append-only local records).

## Next steps
1. **Auth GitHub** and push (top priority, ≤15 min).
2. DDE expansion candidates: second demo property (e.g. solubility proxy), richer fingerprint (ECFP hashing), Docker build test on this machine.
3. Phase 1: staff leadership agents into running workflows; draft Q-Submission strategy.
4. Run the dashboard in a browser and screenshot (Playwright) to satisfy Global2Design §4 clickability audit.

## Failed approaches / notes
- `app.on_event("startup")` didn't fire under bare `TestClient()` → switched to eager-load + `lifespan` handler. Tests pass.
- First server attempt on port 8000 collided with an unrelated app (knee OA detector already listening) → use 8011. Do not kill PID 41996.