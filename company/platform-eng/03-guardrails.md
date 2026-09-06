# Software & Platform Engineering — Guardrails

These are non-negotiable rules. Every agent in the department must follow them. Violations block merges.

---

## GR-1: No Secrets in Code

| Rule | Detail |
|---|---|
| **What** | API keys, database passwords, tokens, certificates, and any credential must never appear in source code, config files, or committed artifacts. |
| **How** | Use environment variables (`os.environ`) or a secrets manager. Reference by key name only: `os.environ["DATABASE_URL"]`. |
| **Enforcement** | Security Engineer runs secret scanning on every PR. CI pipeline blocks commits containing patterns like `password=`, `sk-`, `token=`, `BEGIN RSA PRIVATE KEY`. |
| **Exception** | Dummy/test values in test fixtures are allowed only if clearly labeled as non-functional (`test_password_placeholder`). |

---

## GR-2: Input Validation Mandatory

| Rule | Detail |
|---|---|
| **What** | Every endpoint must validate all input using Pydantic models before any processing occurs. |
| **How** | Define a Pydantic `BaseModel` for every request body, query parameter set, and path parameter. Use `Field(...)` constraints (`min_length`, `max_length`, `gt`, `lt`, `regex`). |
| **Why** | Unvalidated input is the primary attack vector. Healthcare data demands strict schema enforcement. |
| **Enforcement** | Code review rejects endpoints with raw `dict` access or missing validation. Tests must include a validation failure case for every endpoint. |

---

## GR-3: Provenance on Every Prediction

| Rule | Detail |
|---|---|
| **What** | Every prediction response must include: `model_version`, `dataset_version`, `trace_id`, and `timestamp`. |
| **How** | The ML client returns these fields from the ML service. If the ML service omits any, the client generates a fallback value (e.g., `trace_id` via UUID4). |
| **Why** | Regulatory traceability (FDA SaMD requirements). Every inference must be reproducible and auditable. |
| **Enforcement** | Integration tests assert presence of all provenance fields. Regulated-AI validates trace completeness before release. |

---

## GR-4: No Bypassing the Regulated-AI Validation Gate

| Rule | Detail |
|---|---|
| **What** | Any code change that touches model selection, prediction logic, validation thresholds, or provenance recording must be reviewed and approved by the Regulated-AI department before merge. |
| **How** | PRs touching `app/services/predictions.py`, `app/ml_client.py`, `app/routers/predictions.py`, or `app/routers/validation.py` are tagged `regulatory-review-required`. Merge is blocked until Regulated-AI approves. |
| **Why** | The Regulated-AI gate is an independent quality function. Platform Engineering implements; Regulated-AI validates. No self-approval on regulated paths. |
| **Enforcement** | CI label check blocks merge without `regulatory-approved` label on tagged PRs. |

---

## GR-5: Clean Layering — ml/ Framework-Free

| Rule | Detail |
|---|---|
| **What** | The `ml/` directory must not import from `app/` or depend on FastAPI, Starlette, Pydantic, or any web framework. |
| **How** | `ml/` uses only: standard library, numpy, pandas, scikit-learn (or equivalent ML stack). `app/` communicates with `ml/` exclusively through `app/ml_client.py`. |
| **Why** | Decoupling allows ML service to run independently (batch jobs, different deployment target, different scaling). Prevents framework coupling from leaking into model code. |
| **Enforcement** | Lint rule or import check in CI: `ml/` files must not contain `from fastapi`, `from starlette`, `from pydantic`, or `from app`. Violations block merge. |

---

## GR-6: Git and Delivery Discipline

| Rule | Detail |
|---|---|
| **What** | Every verified working change commits immediately with a conventional commit message. |
| **How** | Format: `<type>(<scope>): <description>` — e.g., `feat(predictions): add batch predict endpoint`. Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`. |
| **Why** | Rollback capability. Audit trail. Synchronization with Obsidian vault and HANDOFF.md. |
| **Enforcement** | CI validates commit message format. Head of Engineering reviews commit hygiene in code review. |

---

## GR-7: Test Before Done

| Rule | Detail |
|---|---|
| **What** | No code change is "done" until: (1) `pytest` passes, (2) `ruff check .` passes, (3) type check passes, (4) new code has tests. |
| **How** | Run Verify Commands after every change. Fix failures before committing. |
| **Why** | Fake-green status is a worse failure than a slow honest one. Healthcare software must be verifiably correct. |
| **Enforcement** | CI pipeline runs all checks on every PR. Head of Engineering rejects PRs with failing checks. |

---

## Summary Table

| ID | Guardrail | Owner | Enforcement |
|---|---|---|---|
| GR-1 | No secrets in code | Security Engineer | Secret scan + CI block |
| GR-2 | Input validation mandatory | Backend Engineer | Code review + test case |
| GR-3 | Provenance on every prediction | MLOps Engineer | Integration test + Regulated-AI |
| GR-4 | Regulated-AI gate respected | Head of Engineering | CI label check |
| GR-5 | ml/ framework-free | MLOps Engineer | Import lint + CI block |
| GR-6 | Git discipline | All agents | CI commit lint |
| GR-7 | Test before done | All agents | CI pipeline gate |

---
_Last updated: 2026-09-06_
