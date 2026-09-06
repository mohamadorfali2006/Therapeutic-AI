# Software & Platform Engineering — Standard Operating Procedures

---

## SOP-A: Backend Handler Pattern

Every endpoint follows a four-layer pattern: **Schema -> Service -> Persistence -> Response**.

### 1. Schema (request validation)
Define a Pydantic model for the request body in `app/models/`:

```python
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    smiles: str = Field(..., min_length=1, max_length=500, description="SMILES string")
    model_id: str = Field(..., description="Registered model identifier")
```

### 2. Service (business logic)
Implement the operation in `app/services/`:

```python
async def run_prediction(request: PredictRequest, ml_client: MLClient) -> PredictionResult:
    model = await ml_client.get_model(request.model_id)
    prediction = await ml_client.predict(model_id=request.model_id, smiles=request.smiles)
    return PredictionResult(
        smiles=request.smiles,
        predicted_logIC50=prediction.value,
        confidence_interval=prediction.ci,
        model_version=model.version,
        dataset_version=model.dataset_version,
        trace_id=prediction.trace_id,
    )
```

### 3. Persistence (if needed)
Write results to database or store via a repository class. Skip if the endpoint is stateless (most prediction endpoints).

### 4. Response
Return a typed Pydantic response model. Never return raw dicts from the service layer.

```python
@router.post("/models/{model_id}/predict", response_model=PredictResponse)
async def predict(model_id: str, request: PredictRequest):
    result = await run_prediction(request, ml_client)
    return PredictResponse(status="succeeded", result=result)
```

**Rules:**
- Router functions are thin: parse, validate, call service, return response.
- Business logic lives in services, not routers.
- Errors are caught and converted to RFC 7807 problem details by middleware.

---

## SOP-B: Adding a New Route

| Step | Action | Files touched |
|---|---|---|
| 1 | Define request/response Pydantic models | `app/models/<domain>.py` |
| 2 | Implement service function | `app/services/<domain>.py` |
| 3 | Create router with endpoint | `app/routers/<domain>.py` |
| 4 | Register router in main app | `app/main.py` |
| 5 | Write tests (happy path + error cases) | `tests/test_api/test_<domain>.py` |
| 6 | Run Verify Commands: `pytest`, `ruff check .`, type check | — |
| 7 | Update API reference | `docs/04-API-REFERENCE.md` |

**Router registration in `app/main.py`:**

```python
from app.routers import predictions
app.include_router(predictions.router, prefix="/v1", tags=["predictions"])
```

**Naming conventions:**
- Router files: plural nouns (`predictions.py`, `models.py`, `jobs.py`)
- Service functions: verb + noun (`run_prediction`, `register_model`, `get_model_metrics`)
- Test files: `test_<module>.py` mirroring the source structure

---

## SOP-C: Testing Requirements

### Framework
- **pytest** as test runner
- **httpx.AsyncClient** (or `TestClient`) for API endpoint testing
- **pytest-asyncio** for async test support

### Test structure per endpoint

```python
# tests/test_api/test_predictions.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_predict_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/models/molgen_v3/predict", json={
            "smiles": "CCOc1ccccc1",
            "model_id": "molgen_v3"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "succeeded"
    assert "model_version" in data
    assert "trace_id" in data

@pytest.mark.asyncio
async def test_predict_missing_smiles():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/models/molgen_v3/predict", json={})
    assert response.status_code == 422
    assert response.json()["type"].endswith("/validation")
```

### Required test coverage

| Category | What to test | Minimum |
|---|---|---|
| Happy path | Correct input -> correct response | Every endpoint |
| Validation | Missing fields, bad types, out-of-range values | Every endpoint |
| Auth | Unauthenticated request -> 401/403 | Every protected endpoint |
| ML service failure | ML service unavailable -> graceful error | Prediction endpoints |
| Provenance | Response includes model_version, dataset_version, trace_id | Prediction endpoints |

### Running tests

```bash
cd product/drug-discovery-engine
pytest tests/ -v --tb=short
ruff check app/ tests/
```

---

## SOP-D: Calling the ML Service Cleanly

### Principle
The backend communicates with the ML service through a single abstraction layer (`ml_client`). The ML service must remain framework-free.

### ML Client interface

```python
# app/ml_client.py
class MLClient:
    """Clean interface to ML service. No FastAPI/Pydantic imports."""

    async def register_model(self, name: str, config: dict) -> ModelMetadata: ...
    async def get_model(self, model_id: str) -> ModelMetadata: ...
    async def get_metrics(self, model_id: str) -> dict: ...
    async def predict(self, model_id: str, smiles: str) -> Prediction: ...
    async def batch_predict(self, model_id: str, smiles_list: list[str]) -> str: ...
    async def get_job(self, job_id: str) -> JobStatus: ...
    async def cancel_job(self, job_id: str) -> None: ...
    async def health_check(self) -> HealthStatus: ...
```

### Calling pattern from service layer

```python
# app/services/predictions.py
async def run_prediction(request: PredictRequest, ml_client: MLClient) -> PredictionResult:
    prediction = await ml_client.predict(
        model_id=request.model_id,
        smiles=request.smiles,
    )
    return PredictionResult(
        smiles=request.smiles,
        predicted_logIC50=prediction.value,
        confidence_interval=prediction.ci,
        model_version=prediction.model_version,
        dataset_version=prediction.dataset_version,
        trace_id=prediction.trace_id,
    )
```

### Rules
1. **One-directional dependency:** `app/` depends on `ml/` interface, never the reverse.
2. **No framework leakage:** `ml_client.py` uses only standard library + httpx. No Pydantic, no Starlette.
3. **Error wrapping:** ML service errors are caught and converted to RFC 7807 responses in the service layer, not in `ml_client`.
4. **Provenance propagation:** `ml_client` must return trace metadata on every call. If ML service omits it, the client generates a fallback trace_id.
5. **Testability:** `ml_client` is mockable. Tests use a `FakeMLClient` that returns canned responses.

---
_Last updated: 2026-09-06_
