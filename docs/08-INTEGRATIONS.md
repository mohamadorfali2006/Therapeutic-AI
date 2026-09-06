# 08-INTEGRATIONS — Therapeutic-AI

## External services & data sources (planned)

| Category | Service / source | Status | Notes |
|---|---|---|---|
| Scientific data | Public (ChEMBL, PDB, Uniprot, PubChem, etc.) | Planned | License-aware ingestion |
| Scientific data | Licensed commercial data | Planned | Contractual, tracked in catalog |
| Compute | GPU cloud (AWS/Azure/GCP) | Planned | Spot + reserved mix |
| Auth | OIDC/OAuth provider | Planned | Clinician + internal SSO |
| Observability | Metrics/tracing/logging | Planned | Ops + FDA audit trail |
| Design assets | AI-generated (Pollinations / native gen) | Planned | No stock photos (policy) |

## AI provider notes
- ML models are in-house (research + product). No external LLM dependency for SaMD clinical functions unless validated under PCCP.
- Internal generative AI used for **visual assets only** in product design.

## MCP servers / agent tooling (development)
- Playwright MCP — visual QA for UI (Global2Design §4 verification).
- shadcn-ui MCP — component/design-system implementation.
- Additional MCPs per task as needed (registered in session; never secret-bearing).

## Secrets policy
- **No keys or credentials** stored in this repo.
- Values live in secrets management (env / vault), referenced by name only.
- See `07-HOW-TO-RUN.md` env table for names.

_Updated as integrations are added._