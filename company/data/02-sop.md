# 02-SOP — Data & Infrastructure procedures

Standard operating procedures (operating model §3, "Skills = SOPs"). Every data/infra task selects the matching SOP; do not improvise.

## SOP-A: Seed dataset versioning + split protocol

Trigger: creating a new dataset version, or regenerating splits for `ml/seed_data.py`.

1. **Pin inputs.** Record dataset `name`, `source`, `license`, `raw_payload_ref`, and a declared `dataset_version` (semver: e.g. `1.3.0`). Every input file is checksummed (SHA-256); the manifest records all checksums.
2. **Deterministic seed.** `seed_data.py` uses a fixed, documented RNG seed baked into the dataset version (no wall-clock or hash-order-dependent logic). Same input checksums -> byte-identical outputs.
3. **Stratified-ish split by hash.** For each record, compute a stable `split_hash = sha256(canonical_form + dataset_version)[0:N]` and map to a bucket (e.g. `dt < 0.7` train, `0.7 <= dt < 0.85` val, `>= 0.85` test). Optionally pre-bucket by scaffold/substructure class so near-identical molecules land in one split; hash assignment is the floor guarantee against leakage.
4. **Lock the test set.** The test split is materialized once as `ml/artifacts/splits/<dataset_version>/test.csv` plus manifest JSON (`train.json`, `val.json`, `test.json`) listing record refs. `test.csv` is frozen: any regeneration must byte-match the stored file or fail loudly (never silently rewrite).
5. **Write split provenance.** Register one `dataset_version` record plus three `data_split` records (train/val/test) via the provenance store (`app/store.py`). Store split manifest hashes and dataset_version in the records.
6. **Verify.** Re-run generation from the same inputs and diff — output must be identical. CI runs this determinism check.

## SOP-B: Provenance recording protocol (every prediction)

Trigger: any DDE prediction, evaluation, or training run that should be traceable.

Record one immutable JSON trace per prediction via `app/store.py` with exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| `trace_id` | string (uuid4) | Unique trace identifier, returned to the caller |
| `timestamp` | ISO-8601 UTC | When the prediction was recorded |
| `model_version` | string | Exact model version used (registry id + version) |
| `dataset_version` | string | Dataset/split version that produced the input (empty for ad-hoc input) |
| `input` | object | Canonical input: `smiles`, plus optional molecular descriptors used |
| `output` | object | Prediction result: `label`/`value`, units if applicable |
| `confidence` | number | Model-reported confidence, `null` if not produced |

Rules: write append-only (one record per prediction, never updated); record before returning the result to the caller (fail the request if the trace cannot be written); record training runs and evaluations in the same store using the same shape so model -> dataset ancestry is one graph.

## SOP-C: Local infra workflow

Trigger: building the image, running the DDE locally, or running CI.

1. **Build.** From `product/drug-discovery-engine/`: `docker build -t therapeutic-ai/dde:local .`
2. **Run.** `docker-compose up --build` — single service running API, ML, and the provenance store (JSON files / SQLite volume). Verify with curl that health/probe routes return HTTP 200 (Verified App URLs Only rule); check logs for errors.
3. **Stop / clean.** `docker-compose down`. Persist `app/data/provenance/` and SQLite via a named volume so traces survive rebuilds.
4. **CI.** `.github/workflows/ci.yml` runs on every push: `docker build`, then in-container lint + tests + integrity checks (split manifest hashes match `test.csv`, provenance records parse and are append-only). Red CI blocks merge.
5. **Environment.** Copy `.env.example` to `.env` for local dev; never commit `.env`. The compose file fails closed if required env vars are missing.