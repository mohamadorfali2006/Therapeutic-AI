# 07-HOW-TO-RUN — Therapeutic-AI

_Status: planned — no application code committed yet. This file will document repo layout, env vars, run/build/deploy once Phase 2 engineering starts._

## Current repo layout
```
Therapeutic-AI/
├── docs/            # All project documentation (this set)
├── org/             # Org design: role descriptions, chart
│   └── roles/       # Department role files
├── AGENTS.md        # Project agent rules (ref global CLAUDE.md)
└── HANDOFF.md       # Session continuity (when updated)
```

## Planned tech stack (Phase 2 decision point)
- **Backend:** Python (FastAPI) for inference/services; Go/Node for platform services.
- **ML:** PyTorch; Ray for distributed training; MLflow for tracking.
- **Data:** Postgres + object storage (weights/data); catalog for lineage.
- **Infra:** Kubernetes (GPU), Terraform; CI/CD pipeline with validation gates.
- **Frontend:** React + shadcn/ui + Framer Motion (per global design stack).

## Environment variables (planned)
| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Primary store |
| `OBJECT_STORE_URL` | Weights/data payloads |
| `GPU_CLUSTER_*` | Compute config |
| `AUTH_*` / `OIDC_*` | Auth provider config |
| `SEGMENT/TELEMETRY_*` | Observability |
| `REGULATORY_MODE` | research vs. locked/SaMD mode toggle |

_No secrets committed to the repo. Names only — values live in secrets management (Phase 2)._

## Run/build/deploy
Documented when code exists (see `01-IMPLEMENTATION-PLAN.md` Phase 2).