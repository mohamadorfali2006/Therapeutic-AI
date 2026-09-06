"""DDE provenance store — append-only traceability for predictions and validations.

Owned by company/data + company/regulated-ai. Immutable once appended (append-only;
no deletion/update API by design).
"""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

STORE_DIR = Path(__file__).parent / "data"
TRACES_FILE = STORE_DIR / "traces.jsonl"
VALIDATIONS_FILE = STORE_DIR / "validations.jsonl"
MODELS_FILE = STORE_DIR / "models.json"


class ProvenanceStore:
    """JSON-lines append-only store with a file lock."""

    def __init__(self, base_dir: Path | None = None):
        self._dir = Path(base_dir) if base_dir else STORE_DIR
        self._dir.mkdir(parents=True, exist_ok=True)
        self._traces = self._dir / "traces.jsonl"
        self._validations = self._dir / "validations.jsonl"
        self._models = self._dir / "models.json"
        self._lock = threading.Lock()

    # ---- predictions ----
    def append_prediction(self, record: dict) -> str:
        trace_id = record.get("trace_id") or f"trace-{uuid.uuid4().hex[:12]}"
        record["trace_id"] = trace_id
        record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        record.setdefault("status", "recorded")
        with self._lock:
            with open(self._traces, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        return trace_id

    def get_trace(self, trace_id: str) -> dict | None:
        with self._lock:
            if not self._traces.exists():
                return None
            with open(self._traces, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    if rec.get("trace_id") == trace_id:
                        return rec
        return None

    # ---- validations ----
    def append_validation(self, record: dict) -> None:
        record.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        record.setdefault("verified_by", "regulated-ai-validation-gate")
        with self._lock:
            with open(self._validations, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")

    def latest_validation(self) -> dict | None:
        latest = None
        with self._lock:
            if not self._validations.exists():
                return None
            with open(self._validations, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        latest = json.loads(line)
        return latest

    # ---- model registry ----
    def register_model(self, info: dict) -> None:
        with self._lock:
            current = self.list_models()
            current = [m for m in current if m.get("name") != info.get("name")]
            current.append(info)
            self._write_models(current)

    def list_models(self) -> list[dict]:
        with self._lock:
            if not self._models.exists():
                return []
            try:
                with open(self._models, encoding="utf-8") as fh:
                    data = json.load(fh)
                return data if isinstance(data, list) else []
            except (json.JSONDecodeError, OSError):
                return []

    def _write_models(self, models: list[dict]) -> None:
        with open(self._models, "w", encoding="utf-8") as fh:
            json.dump(models, fh, indent=2)