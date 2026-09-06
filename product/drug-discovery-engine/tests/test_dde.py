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
    assert r.json()["predictor_ready"] is True


def test_predict_valid_smiles_logp():
    r = client.post("/api/v1/predict", json={"smiles": "CCO"})
    assert r.status_code == 200
    body = r.json()
    assert body["trace_id"].startswith("trace-")
    assert body["model_version"]
    assert body["dataset_version"]
    assert body["property"] == "logp"
    assert "value" in body["output"]
    assert "research use only" in body["disclaimer"].lower()


def test_predict_valid_smiles_logS():
    r = client.post("/api/v1/predict", json={"smiles": "CCO", "property": "logS"})
    assert r.status_code == 200
    body = r.json()
    assert body["property"] == "logS"
    assert "value" in body["output"]
    assert body["model_name"] == "baseline-logS"


def test_predict_valid_smiles_tpsa():
    r = client.post("/api/v1/predict", json={"smiles": "CCO", "property": "tpsa"})
    assert r.status_code == 200
    body = r.json()
    assert body["property"] == "tpsa"
    assert "value" in body["output"]
    assert body["model_name"] == "baseline-tpsa"


def test_predict_unknown_property_503():
    r = client.post("/api/v1/predict", json={"smiles": "CCO", "property": "nope"})
    assert r.status_code == 503


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


def test_trace_roundtrip_logS():
    pred = client.post(
        "/api/v1/predict", json={"smiles": "c1ccccc1", "property": "logS"}
    ).json()
    r = client.get(f"/api/v1/traces/{pred['trace_id']}")
    assert r.status_code == 200
    assert r.json()["trace"]["property"] == "logS"


def test_trace_not_found():
    r = client.get("/api/v1/traces/nope-123")
    assert r.status_code == 404


def test_models_list_has_both_properties():
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    names = {m["name"] for m in r.json()["models"]}
    assert {"baseline-logp", "baseline-logS"} <= names


def test_validate_gate_pass_single_property():
    r = client.post("/api/v1/validate?property=logp")
    assert r.status_code == 200
    report = r.json()["report"]
    assert "r2" in report
    assert "mae" in report
    assert "passed" in report
    assert isinstance(report["passed"], bool)


def test_validate_all_models_returns_each():
    r = client.post("/api/v1/validate")
    assert r.status_code == 200
    report = r.json()["report"]
    assert isinstance(report, list)
    assert len(report) >= 2
    assert all(x["passed"] for x in report)


def test_validate_default_artifacts_present():
    from ml.baseline import load_all

    preds = load_all()
    assert preds, "model artifacts must exist after training"


def test_fingerprint_deterministic_and_size():
    from ml.fingerprints import smiles_to_fingerprint

    assert smiles_to_fingerprint("CCO") == smiles_to_fingerprint("CCO")
    assert len(smiles_to_fingerprint("CCO")) == 256
    assert smiles_to_fingerprint("CCO") != smiles_to_fingerprint("CC(=O)O")


def test_ui_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "Drug Discovery Engine" in r.text