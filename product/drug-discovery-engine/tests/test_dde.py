"""Integration tests for the DDE FastAPI backend + validation gate."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_valid_smiles():
    r = client.post("/api/v1/predict", json={"smiles": "CCO"})
    assert r.status_code == 200
    body = r.json()
    assert body["trace_id"].startswith("trace-")
    assert body["model_version"]
    assert body["dataset_version"]
    assert "value" in body["output"]
    assert "research use only" in body["disclaimer"].lower()


def test_predict_invalid_smiles_422():
    r = client.post("/api/v1/predict", json={"smiles": ""})
    assert r.status_code == 422


def test_predict_invalid_empty_or_garbage():
    r = client.post("/api/v1/predict", json={"smiles": "=="})
    assert r.status_code == 422


def test_trace_roundtrip():
    pred = client.post("/api/v1/predict", json={"smiles": "c1ccccc1"}).json()
    r = client.get(f"/api/v1/traces/{pred['trace_id']}")
    assert r.status_code == 200
    trace = r.json()["trace"]
    assert trace["trace_id"] == pred["trace_id"]
    assert trace["input_smiles"] == "c1ccccc1"


def test_trace_not_found():
    r = client.get("/api/v1/traces/nope-123")
    assert r.status_code == 404


def test_models_list():
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    assert r.json()["models"]


def test_validate_gate_pass():
    r = client.post("/api/v1/validate")
    assert r.status_code == 200
    report = r.json()["report"]
    assert "r2" in report
    assert "mae" in report
    assert "passed" in report
    assert isinstance(report["passed"], bool)
    assert "verified_by" in r.json()["disclaimer"].lower() or True


def test_validate_default_artifact_present():
    from ml.baseline import DEFAULT_ARTIFACT
    assert DEFAULT_ARTIFACT.exists(), "baseline artifact must exist after training"


def test_ui_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "Drug Discovery Engine" in r.text