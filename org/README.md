# org/ — Org Design for Therapeutic-AI

## Overview
Enterprise (84-role) structure for an AI drug-discovery company that also ships FDA-cleared SaMD.

| # | Function | Headcount |
|---|---|---|
| 1 | Executive Leadership | 6 |
| 2 | AI Research & ML | 14 |
| 3 | Computational Drug Discovery | 10 |
| 4 | Wet Lab / Biology | 8 |
| 5 | Software & Platform Engineering | 14 |
| 6 | Regulated AI / ML-Validation | 8 |
| 7 | Regulatory, Quality & Clinical | 10 |
| 8 | Data & Infrastructure | 6 |
| 9 | Business / GTM / Ops | 8 |
| **Total** | | **84** |

## Reporting structure (summary)
```
CEO
├── CSO
│   ├── Computational Drug Discovery
│   └── Wet Lab / Biology
├── CTO
│   ├── AI Research & ML
│   ├── Software & Platform Engineering
│   └── Data & Infrastructure
│       └── (matrixed) Regulated AI / ML-Validation
├── CMO
│   └── Clinical Affairs
├── CRQO
│   ├── Regulated AI / ML-Validation (matrix with CTO)
│   └── Regulatory Affairs + QA/QMS
└── COO
    └── Business / GTM / Ops
```

## Files
- `roles/01-…09-*.md` — detailed role descriptions per function.
- See `docs/01-IMPLEMENTATION-PLAN.md` for phased hiring roadmap.