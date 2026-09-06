# 05-DATABASE — Therapeutic-AI (Planned)

_Status: planned. Schema finalized in Phase 2; this is the data-model design intent._

## Core requirements
1. **Provenance** — every training datum, every model, every prediction traceable.
2. **Training/test separation** — locked splits; no leakage; auditable.
3. **Regulatory traceability** — map dataset → model version → validation → release.

## Logical data model (planned)

### Datasets
| Entity | Fields (planned) | Purpose |
|---|---|---|
| `dataset` | id, name, source (public/licensed/wet-lab), license, version, checksum | Registry of all data |
| `dataset_version` | id, dataset_id, snapshot_ref, created_at, provenance_json | Versioned snapshots |
| `data_record` | id, dataset_version_id, modality, canonical_form (SMILES/seq/seq), raw_payload_ref | Individual records |
| `data_split` | id, dataset_version_id, split_name (train/val/test), record_id | Locked splits, auditable |

### Models
| Entity | Fields (planned) | Purpose |
|---|---|---|
| `model` | id, name, type (foundation/task), architecture, status (research/frozen/retiring) | Model registry |
| `model_version` | id, model_id, weights_ref, config_ref, dataset_version_id, metrics_json, created_at | Versioned weights + training data provenance |
| `evaluation` | id, model_version_id, eval_split_ref, metrics_json, pass/fail | Evaluation records (locked splits) |

### Inference / Trace
| Entity | Fields (planned) | Purpose |
|---|---|---|
| `inference` | id, job_id, model_version_id, input_ref, output_ref, confidence, trace_id | Every prediction traceable |
| `clinical_analysis` | id, clinician_id, inference_id, report_ref, status, audit_ref | SaMD clinical record (PHI) |

### Regulatory / QMS
| Entity | Fields (planned) | Purpose |
|---|---|---|
| `release` | id, software_version, model_version_ids, validation_report_ref, status, approved_by | Release gate |
| `pccp_change` | id, pccp_id, change_type, validation_evidence_ref, status | PCCP-tracked modifications |
| `capa` / `audit_log` | id, type, ref, resolution | QMS trail |

## Security / privacy
- Clinical data (PHI) encrypted at rest + in transit; access-scoped; audit-logged.
- Training data licensing tracked; no PHI in research datasets without governance approval.
- Backup/retention per regulatory + internal policy.

## Tooling (planned)
- Relational store for registry/lineage (e.g., Postgres); object store for payloads/weights; feature store for serving.
- Catalog tool for lineage (e.g., DataHub/OpenMetadata-style) — decided in Phase 2.

_Subject to change during Phase 2 engineering._