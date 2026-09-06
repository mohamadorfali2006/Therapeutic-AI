# 00-CHARTER — Data & Infrastructure Department

_Reports to: CTO. Masters: datasets, provenance, local infra._

## 1. Mission

Provide the **regulated-data foundation** for the Drug Discovery Engine (DDE): every datum, every split, every model, and every prediction is provably traceable. Without clean, versioned, license-aware data and immutable traces, both the science and the FDA evidence collapse.

## 2. Scope

| Domain | Owns | DDE artifact |
|---|---|---|
| Dataset governance | Versioning, licensing, checksums, catalog | `ml/seed_data.py` split logic + split manifests |
| Split discipline | Train/val/test separation, no leakage, locked test set | `ml/artifacts/splits/`, `ml/artifacts/datasets/` |
| Prediction traceability | Every prediction recorded with full context | Provenance store `app/store.py` + trace JSON records |
| Local persistence | JSON-file / SQLite-backed provenance store | `app/store.py`, `app/data/provenance/` |
| Infra | Reproducible local run of the DDE | `Dockerfile`, `docker-compose.yml`, CI workflow, `.env.example` |

## 3. Principles

1. **Provenance everywhere** (operating model §3.5, GMP-grade traceability): anything touching models, data, or regulatory surfaces must be reproducible and provable. No unrecorded change to a dataset or model matters; an unrecorded prediction does not count.
2. **Splits are sacred**: a test set is written once, frozen, checksummed, and never touched by training—directly or transitively (no hyper-parameter tuning on test, no deduplication after split).
3. **Immutable append-only traces**: provenance records are never edited or deleted in place; corrections are written as new records.
4. **Locally reproducible**: the whole DDE runs on one machine via Docker Compose; CI enforces the same gates locally.
5. **Version everything, pin the versions you ship**: dataset versions, model versions, and split manifest hashes are first-class fields on every artifact and every trace.

## 4. Department contract (what we deliver, per operating model §6)

- `ml/seed_data.py` — deterministic, versioned dataset builder that emits split manifests and locked test sets.
- `app/store.py` — provenance store module (JSON-file and SQLite backends, append-only API).
- `app/data/provenance/*.json` — immutable trace records (one per prediction).
- `product/drug-discovery-engine/Dockerfile` and `docker-compose.yml` — single-service image used by API, ML, and provenance.
- CI workflow (`.github/workflows/ci.yml`) — build, lint, and tests, plus provenance/split integrity checks.
- `.env.example` — documented env template; real `.env` is never committed.

## 5. Relationship to other departments

- **AI Research & ML** consumes datasets/splits and emits model versions; we record their provenance, we do not own model tuning.
- **Regulated AI / ML-Validation** signs off on anything touching model/validation logic; we guarantee the split and trace evidence they review.
- **Platform Engineering** owns the API surface; the provenance store is a platform service owned by us (`app/store.py`).

## 6. Definition of done (department)

A dataset, trace, or infra change is done only when: versioned, checksummed, recorded in the provenance store, tests/lint pass, committed with a conventional message.

_Last updated: 2026-09-06_