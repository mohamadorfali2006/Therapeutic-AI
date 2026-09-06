# HANDOFF — Therapeutic-AI

**Session date:** 2026-09-06 (updated at end of Sprint S1 — company platform live)

## What was accomplished

### Round 1 — Scaffolding
- Scaffolded `C:/Users/PCD/Therapeutic-AI` with full org design (84 roles, 9 functions, `org/`) and documentation set (`docs/00-INDEX` → `10-CHANGELOG`).
- Initial git history: `d8460dd` scaffold, `e1921fd` handoff.

### Round 2 — Agent-based company + working product
- **Agent company (`company/`)**: 9 departments staffed with specialist AI agents — leadership, ai-research, cdd, wetlab, platform-eng, regulated-ai, regulatory, data, business. Each has `00-charter.md`, `01-agents.md` (YAML roster), `02-sop.md`, `03-guardrails.md`. Master constitution: `company/00-OPERATING-MODEL.md`.
- **Drug Discovery Engine (DDE) MVP** (`product/drug-discovery-engine/`) — the single primary product: FastAPI backend, pure-Python ML, append-only provenance, validation gate, web dashboard, Docker/CI.
- Commits: `4ba5a0d` (company + DDE MVP), `0f74df6` (docs), `8ce59c1` (HANDOFF), `39597e1` (Playwright QA).
- Visual QA 12/12; validation gate PASS (logP-only, R2=0.6583).

### Round 3 — Company platform RUNS (Sprint S1, this session)
- **`company/platform/run.py`** — company runtime CLI (stdlib only): `sprint plan/list/close`, `task add/start/done/block`, `gate <id> --pass`, `status`, `report --out`. Persistent board: `company/platform/state.json`.
- **Sprint S1 → DDE v0.2.0**, executed live, closed **7/7 tasks / 7/7 gates PASS**:
  - logS dataset v2 (`ml/logs_data.py`, 57 compounds, CDD spec, Data provenance docs)
  - ECFP-style hashed fingerprints (`ml/fingerprints.py`, radius 2, 256 bits, pure Python) — raised logP R2 0.658→0.722
  - Property-aware trainer (`ml/baseline.py`) + property-routed API (`/api/v1/predict` with `property`; `/api/v1/validate?property=`)
  - Regulated-AI gate report: `company/regulated-ai/reports/2026-09-06-s1-gates.md` (both models PASS)
  - Regulatory product status: `company/regulatory/04-product-status.md`
  - Sprint report: `company/platform/sprint-S1-report.md`
- **Verified:** 15/15 pytest, both gates PASS (logp R2=0.7222, logS R2=0.6079), live routes 200, Playwright QA **14/14** (incl. property dropdown routing).
- Commits: `2a83798` (Sprint S1). **Latest: `2a83798`.**

## Key constraints / current state
- Server normally on **port 8011** (8000 occupied by unrelated knee-OA app, PID varies — never kill it).
- venv: `C:\Users\PCD\Therapeutic-AI\.venv` (`py -3.13`). Train with `.venv\Scripts\python.exe -m ml.train` from `product/drug-discovery-engine`.
- Provenance `app/data/*.jsonl` is gitignored (runtime records).
- Single product = DDE; research-use only, NOT a medical device. PCCP-first posture for future adaptive retraining.

## Blockers / next steps
- **GitHub push still blocked**: `gh` CLI not installed, no `GH_TOKEN`, no winget. Recovery: install gh → `gh auth login` → `gh repo create Therapeutic-AI --private --source=. --remote=origin --push`.
- Next sprint candidates (S2): staff Leadership/CEO loop against DDE roadmap, add a 3rd property or real-vs-predicted scatter QA, Docker artifact baking, PCCP pipeline draft (regulatory).

## How to run the company
```powershell
.\.venv\Scripts\python.exe company\platform\run.py sprint plan --name "S2 ..." --goal "..."
.\.venv\Scripts\python.exe company\platform\run.py task add --dept ai-research --title "..."
.\.venv\Scripts\python.exe company\platform\run.py gate T1 --pass --evidence "..."
.\.venv\Scripts\python.exe company\platform\run.py status   # board
```

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