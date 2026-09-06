# Docker Build Guide — Drug Discovery Engine

**Author:** Platform Engineer Agent (company/platform-eng)
**Date:** 2026-09-06
**Status:** Phase 2 deliverable — multi-stage Dockerfile with artifact baking

---

## 1. Overview

The DDE Docker image uses a multi-stage build to bake model artifacts into the
image so the API works out of the box — no runtime training required.

## 2. Build stages

### Stage 1: Training
- Installs all dependencies (including training requirements)
- Copies ML source code
- Runs `python -m ml.train` to produce all model artifacts
- Output: `ml/artifacts/*.pkl` + `*_meta.json`

### Stage 2: Runtime
- Smaller base image (no build tools)
- Copies only runtime requirements
- Copies application code + web dashboard
- **Copies trained artifacts from Stage 1** (`COPY --from=training`)
- Includes health check endpoint

## 3. Build command

```bash
cd product/drug-discovery-engine
docker build -t dde:latest .
```

## 4. Run command

```bash
docker run -d -p 8000:8000 --name dde dde:latest
```

## 5. Verify

```bash
curl http://localhost:8000/health
# {"status":"ok","predictor_ready":true}

curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"smiles":"CCO","property":"tpsa"}'
# {"trace_id":"trace-...","model_version":"baseline-v1.0.0",...}
```

## 6. CI/CD integration

The GitHub Actions workflow (`.github/workflows/ci.yml`) includes a Docker job
that builds and tests the image on every push to master:

```yaml
docker:
  runs-on: ubuntu-latest
  needs: validation-gate
  if: github.event_name == 'push' && github.ref == 'refs/heads/master'
  steps:
    - uses: actions/checkout@v4
    - name: Build Docker image
      run: docker build -t dde:${{ github.sha }} .
    - name: Test Docker image
      run: |
        docker run -d -p 8000:8000 --name dde-test dde:${{ github.sha }}
        sleep 5
        curl -f http://localhost:8000/health || exit 1
        docker stop dde-test
```

## 7. Notes

- Docker daemon must be running to build locally
- CI builds and tests the image automatically
- Artifacts are baked in — no runtime training needed
- Image size is minimized by multi-stage build (training deps not included)
