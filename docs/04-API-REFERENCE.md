# 04-API-REFERENCE — Therapeutic-AI (Planned)

_Status: planned. Endpoints defined as part of Phase 2 engineering; refined as implementation proceeds._

## Conventions
- Base URL: `https://api.therapeutic-ai.com/v1` (production); `https://staging.api.therapeutic-ai.com/v1` (staging).
- Format: JSON over HTTPS. Auth: OAuth2 / client credentials (service), JWT (user sessions).
- Versioned; breaking changes require new major version.
- All inference endpoints return model version + trace metadata (provenance requirement).

---

## Research / Drug Discovery Platform

### Models
| Method | Path | Description |
|---|---|---|
| `POST` | `/models` | Register a model (weights, config, dataset version) |
| `GET` | `/models/{id}` | Model metadata + version history |
| `GET` | `/models/{id}/metrics` | Evaluation metrics (locked splits) |

### Prediction / Inference
| Method | Path | Description |
|---|---|---|
| `POST` | `/models/{id}/predict` | Run inference (property, docking, generation) |
| `POST` | `/models/{id}/batch-predict` | Batch inference (async job id returned) |

### Jobs
| Method | Path | Description |
|---|---|---|
| `GET` | `/jobs/{id}` | Job status + result |
| `POST` | `/jobs/{id}/cancel` | Cancel running job |

---

## SaMD Clinical Product

### Auth
| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Clinician login (JWT + MFA) |
| `POST` | `/auth/refresh` | Refresh token |
| `POST` | `/auth/logout` | Revoke session |

### Analysis (locked model endpoints)
| Method | Path | Description |
|---|---|---|
| `POST` | `/analysis` | Submit clinical input for validated analysis |
| `GET` | `/analysis/{id}` | Retrieve result + model version + confidence |
| `GET` | `/analysis/{id}/report` | Generated clinical report (PDF/HL7) |

### Health / Monitoring
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness |
| `GET` | `/health/ready` | Readiness (dependencies) |
| `GET` | `/metrics` | Ops/metrics (authenticated, internal) |

---

## Example: prediction request response
```json
{
  "job_id": "job_abc123",
  "model_id": "molgen_v3",
  "model_version": "2026-08-21-17a",
  "dataset_version": "chemostar_2026.2",
  "status": "succeeded",
  "result": {
    "smiles": "CCOc1ccccc1",
    "predicted_logIC50": 6.4,
    "confidence_interval": [5.8, 7.0]
  }
}
```

## Errors
- Standard RFC 7807 problem details:
```json
{ "type": "https://api.therapeutic-ai.com/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "detail": "field 'input' is required",
  "trace_id": "req_xyz" }
```