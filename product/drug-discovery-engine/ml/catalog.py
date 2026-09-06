"""DDE Data Catalog + Lineage System (v1).

Provides:
- Dataset registry (versioned, immutable)
- Data lineage tracking (dataset → split → features → model → prediction)
- Split integrity verification (locked splits, checksums)
- JSONL-based append-only catalog storage

Phase 1: file-based catalog. Phase 2: migrate to DataHub/OpenMetadata.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CATALOG_DIR = Path(__file__).resolve().parent.parent / "app" / "data"
CATALOG_FILE = CATALOG_DIR / "catalog.jsonl"
SPLIT_REGISTRY_FILE = CATALOG_DIR / "split_registry.jsonl"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def _sha256_str(s: str) -> str:
    """Compute SHA-256 hash of a string."""
    return f"sha256:{hashlib.sha256(s.encode()).hexdigest()}"


class DatasetRegistry:
    """Register and version datasets."""

    def __init__(self, catalog_file: Path = CATALOG_FILE):
        self.catalog_file = catalog_file
        self.catalog_file.parent.mkdir(parents=True, exist_ok=True)

    def register(
        self,
        dataset_id: str,
        name: str,
        source: str,
        license: str,
        version: str,
        records: int,
        properties: list[str],
        checksum: str,
        description: str = "",
    ) -> dict[str, Any]:
        """Register a new dataset version."""
        entry = {
            "type": "dataset_version",
            "dataset_id": dataset_id,
            "name": name,
            "source": source,
            "license": license,
            "version": version,
            "records": records,
            "properties": properties,
            "checksum": checksum,
            "description": description,
            "created_at": _utcnow(),
        }
        self._append(entry)
        return entry

    def _append(self, entry: dict[str, Any]) -> None:
        """Append an entry to the catalog."""
        with open(self.catalog_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_datasets(self) -> list[dict[str, Any]]:
        """Get all dataset entries."""
        return self._read_all()

    def get_dataset(self, dataset_id: str, version: str) -> dict[str, Any] | None:
        """Get a specific dataset version."""
        for entry in self._read_all():
            if (
                entry.get("type") == "dataset_version"
                and entry.get("dataset_id") == dataset_id
                and entry.get("version") == version
            ):
                return entry
        return None

    def _read_all(self) -> list[dict[str, Any]]:
        """Read all entries from the catalog."""
        if not self.catalog_file.exists():
            return []
        entries = []
        with open(self.catalog_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries


class SplitRegistry:
    """Manage locked train/test splits with integrity verification."""

    def __init__(self, registry_file: Path = SPLIT_REGISTRY_FILE):
        self.registry_file = registry_file
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)

    def register_split(
        self,
        dataset_id: str,
        dataset_version: str,
        split_name: str,
        n_records: int,
        checksum: str,
        split_seed: int = 42,
    ) -> dict[str, Any]:
        """Register a locked split."""
        entry = {
            "type": "data_split",
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "split_name": split_name,
            "n_records": n_records,
            "checksum": checksum,
            "split_seed": split_seed,
            "created_at": _utcnow(),
        }
        self._append(entry)
        return entry

    def verify_split(
        self,
        dataset_id: str,
        dataset_version: str,
        split_name: str,
        current_checksum: str,
    ) -> tuple[bool, list[str]]:
        """Verify split integrity against registry."""
        errors = []
        entry = self.get_split(dataset_id, dataset_version, split_name)
        if entry is None:
            errors.append(f"No split registered for {dataset_id}/{dataset_version}/{split_name}")
            return False, errors

        if entry["checksum"] != current_checksum:
            errors.append(
                f"Checksum mismatch for {dataset_id}/{dataset_version}/{split_name}: "
                f"registry={entry['checksum']}, current={current_checksum}"
            )
            return False, errors

        return True, []

    def get_split(
        self, dataset_id: str, dataset_version: str, split_name: str
    ) -> dict[str, Any] | None:
        """Get a specific split entry."""
        for entry in self._read_all():
            if (
                entry.get("type") == "data_split"
                and entry.get("dataset_id") == dataset_id
                and entry.get("dataset_version") == dataset_version
                and entry.get("split_name") == split_name
            ):
                return entry
        return None

    def get_splits_for_dataset(
        self, dataset_id: str, dataset_version: str
    ) -> list[dict[str, Any]]:
        """Get all splits for a dataset version."""
        return [
            entry
            for entry in self._read_all()
            if entry.get("type") == "data_split"
            and entry.get("dataset_id") == dataset_id
            and entry.get("dataset_version") == dataset_version
        ]

    def _append(self, entry: dict[str, Any]) -> None:
        """Append an entry to the registry."""
        with open(self.registry_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _read_all(self) -> list[dict[str, Any]]:
        """Read all entries from the registry."""
        if not self.registry_file.exists():
            return []
        entries = []
        with open(self.registry_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries


class LineageTracker:
    """Track data lineage from dataset → model → prediction."""

    def __init__(self, catalog_file: Path = CATALOG_FILE):
        self.catalog_file = catalog_file
        self.catalog_file.parent.mkdir(parents=True, exist_ok=True)

    def log_training_run(
        self,
        run_id: str,
        dataset_id: str,
        dataset_version: str,
        split_name: str,
        model_id: str,
        model_version: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Log a training run (dataset → model lineage)."""
        entry = {
            "type": "training_run",
            "run_id": run_id,
            "dataset_id": dataset_id,
            "dataset_version": dataset_version,
            "split_name": split_name,
            "model_id": model_id,
            "model_version": model_version,
            "params": params,
            "timestamp": _utcnow(),
        }
        self._append(entry)
        return entry

    def log_prediction(
        self,
        trace_id: str,
        model_id: str,
        model_version: str,
        input_smiles: str,
        output: dict[str, Any],
    ) -> dict[str, Any]:
        """Log a prediction (model → prediction lineage)."""
        entry = {
            "type": "prediction",
            "trace_id": trace_id,
            "model_id": model_id,
            "model_version": model_version,
            "input_smiles": input_smiles,
            "output": output,
            "timestamp": _utcnow(),
        }
        self._append(entry)
        return entry

    def get_model_lineage(self, model_id: str, model_version: str) -> dict[str, Any] | None:
        """Get full lineage for a model version."""
        lineage = None
        predictions = []
        for entry in self._read_all():
            if entry.get("type") == "training_run" and entry.get("model_id") == model_id and entry.get("model_version") == model_version:
                lineage = entry
            elif entry.get("type") == "prediction" and entry.get("model_id") == model_id and entry.get("model_version") == model_version:
                predictions.append(entry)
        if lineage:
            lineage["predictions"] = predictions
        return lineage

    def _append(self, entry: dict[str, Any]) -> None:
        """Append an entry to the catalog."""
        with open(self.catalog_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _read_all(self) -> list[dict[str, Any]]:
        """Read all entries from the catalog."""
        if not self.catalog_file.exists():
            return []
        entries = []
        with open(self.catalog_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries


def get_catalog_summary() -> dict[str, Any]:
    """Get a summary of the current catalog state."""
    catalog = DatasetRegistry()
    splits = SplitRegistry()
    lineage = LineageTracker()

    datasets = [e for e in catalog._read_all() if e.get("type") == "dataset_version"]
    split_entries = [e for e in splits._read_all() if e.get("type") == "data_split"]
    training_runs = [e for e in lineage._read_all() if e.get("type") == "training_run"]
    predictions = [e for e in lineage._read_all() if e.get("type") == "prediction"]

    return {
        "n_datasets": len(datasets),
        "n_splits": len(split_entries),
        "n_training_runs": len(training_runs),
        "n_predictions": len(predictions),
        "datasets": datasets,
        "splits": split_entries,
    }


if __name__ == "__main__":
    import sys

    print("DDE Data Catalog + Lineage System — Status")
    print("=" * 50)

    summary = get_catalog_summary()
    print(f"  Datasets:       {summary['n_datasets']}")
    print(f"  Splits:         {summary['n_splits']}")
    print(f"  Training runs:  {summary['n_training_runs']}")
    print(f"  Predictions:    {summary['n_predictions']}")

    sys.exit(0)
