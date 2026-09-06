# Software & Platform Engineering — Charter

## Mission

Ship the Drug Discovery Engine (DDE) as production-grade software: a FastAPI backend, web dashboard, and clean integration layer between the API and ML service. Own code quality, reliability, and delivery velocity for the platform that researchers and clinicians depend on.

## Scope

| Area | Owned path | What we own |
|---|---|---|
| Backend API | `product/drug-discovery-engine/app/` | FastAPI application, routers, models, services, middleware |
| Web Dashboard | `product/drug-discovery-engine/web/` | Frontend app (React + shadcn/ui + Framer Motion) |
| Integration | `app/ml_client.py` (or equivalent) | Clean interface between backend and ML service |
| Tests | `product/drug-discovery-engine/tests/` | Backend + integration test suite |
| CI/Infra | `Dockerfile`, CI workflows | Build, lint, test pipelines |

**Not owned:** ML model internals (`ml/`), regulatory validation logic (`regulated-ai/`), wet-lab experiments, business strategy. We serve those teams via clean interfaces.

## API Contract with ML Service

The backend is the single entry point for all prediction requests. It delegates to the ML service through a well-defined boundary:

```
Client -> app/routers/ -> app/services/ -> ml_client -> ml/ predictor
```

| Backend endpoint (app/) | Calls ML service | Returns |
|---|---|---|
| `POST /models` | `ml.register_model()` | Model metadata + version |
| `GET /models/{id}` | `ml.get_model()` | Model info + version history |
| `GET /models/{id}/metrics` | `ml.get_metrics()` | Evaluation metrics (locked splits) |
| `POST /models/{id}/predict` | `ml.predict()` | Prediction result + trace |
| `POST /models/{id}/batch-predict` | `ml.batch_predict()` | Async job ID |
| `GET /jobs/{id}` | `ml.get_job()` | Job status + result |
| `POST /jobs/{id}/cancel` | `ml.cancel_job()` | Cancellation confirmation |
| `GET /health` | (none) | Liveness |
| `GET /health/ready` | `ml.health_check()` | Readiness with dependency status |

**Contract rules:**
- Backend never imports from `ml/` directly. Communication goes through `ml_client` (HTTP calls or in-process interface, depending on deployment mode).
- Every prediction response includes `model_version`, `dataset_version`, and `trace_id` — this is a provenance requirement, not optional.
- Errors from ML service are wrapped in RFC 7807 problem details before reaching the client.
- ML service is dependency-free of FastAPI/Starlette/Pydantic. The boundary is one-directional: `app/ -> ml/`, never the reverse.

## Engineering Quality Bar

1. **Build/lint/test pass** before any merge. No exceptions.
2. **Type hints everywhere** — backend code is fully typed; mypy or pyright enforced in CI.
3. **Input validation** — every endpoint validates via Pydantic models. No raw dict access.
4. **Error handling** — structured RFC 7807 responses. No stack traces to clients.
5. **Provenance** — every prediction response carries model version, dataset version, trace ID, and timestamp.
6. **Test coverage** — all routers tested with `pytest` + `httpx.TestClient`. Integration tests cover the backend-to-ML boundary.
7. **Security** — no secrets in code. Environment variables for all config. SBOM maintained.
8. **Documentation** — every new endpoint gets a docstring + OpenAPI schema. API reference stays current.
9. **Git discipline** — conventional commits. Every verified change committed immediately.
10. **Escalation** — if a blocker cannot be self-resolved, raise to Head of Engineering, then to CTO.

---
_Last updated: 2026-09-06_
