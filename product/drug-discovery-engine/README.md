# Drug Discovery Engine — run book (research platform foundation)

## Prereqs
- Python 3.13 (py -3.13 on Windows) with packages in `requirements.txt`.

## Setup
```bash
cd product/drug-discovery-engine
py -3.13 -m pip install -r requirements.txt
```

## Train baseline model (AI Research / CDD-demo)
```bash
py -3.13 -m ml.train
```
Persists `ml/artifacts/baseline_v1.pkl` + `baseline_v1_meta.json`.

## Evaluate + validation gate
```bash
py -3.13 -m ml.evaluate
```

## Run the API
```bash
py -3.13 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
- Dashboard: http://localhost:8000/
- Docs: http://localhost:8000/docs

## Test
```bash
py -3.13 -m pytest tests -q
```

## Verify UI (Visual QA / clickability audit)
With the server running on 8011:
```bash
py -3.13 -m pip install playwright
py -3.13 -m playwright install chromium
py -3.13 tests/qa_dashboard.py
```
Runs a Playwright audit: title, health indicator, models table, predict flow,
theme toggle (dark/light), trace fetch, invalid-SMILES 422. Screenshots saved to
`tests/qa-screenshots/`.

## Docker
```bash
docker build -t dde .
docker run -p 8000:8000 dde
# then run `docker exec -it <cid> python -m ml.train` once to create the artifact,
# or bake the artifact into the image (Dockerfile.training stage).
```

## CI
`.github/workflows/ci.yml` runs install → train → test → validate.

## Notes
- Provenance records accumulate in `app/data/*.jsonl` (append-only).
- Research use only. Not a medical device.