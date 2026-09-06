"""DDE backend — FastAPI application.

Single primary product: Drug Discovery Engine research platform foundation.
Serves the API + static web dashboard. Research use only (not a medical device).
"""

from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import ml
from ml.baseline import DATASET_VERSION, MODEL_VERSION, BaselinePredictor, load_default
from ml.evaluate import run_validation

from .store import ProvenanceStore

logger = logging.getLogger("ddengine")
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

HERE = Path(__file__).parent
WEB_DIR = HERE.parent / "web"

DISCLAIMER = (
    "For research use only. Not a medical device. Outputs are demonstration-grade "
    "model predictions and must not inform clinical decisions."
)


class PredictRequest(BaseModel):
    smiles: str = Field(..., min_length=1, max_length=512, description="SMILES string")
    property: str = Field("logp", description="demo property id")


class PredictResponse(BaseModel):
    trace_id: str
    model_name: str
    model_version: str
    dataset_version: str
    input_smiles: str
    output: dict[str, Any]
    disclaimer: str


class ValidateResponse(BaseModel):
    report: dict[str, Any]
    disclaimer: str


class TraceResponse(BaseModel):
    trace: dict[str, Any] | None


class ModelsResponse(BaseModel):
    models: list[dict[str, Any]]


def _load_predictor() -> BaselinePredictor | None:
    try:
        p = load_default()
        logger.info("Predictor loaded: %s (%s)", p.version, p.dataset_version)
        return p
    except FileNotFoundError:
        logger.warning("No model artifact found — run `python -m ml.train`.")
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Eager-load at startup AND init state here so TestClient() without a
    # context manager still has predictor_ready defined.
    app.state.predictor = _load_predictor()
    app.state.predictor_ready = app.state.predictor is not None
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Drug Discovery Engine",
        version="0.1.0",
        description="AI drug discovery research platform foundation (research use only).",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.store = ProvenanceStore()
    app.state.predictor = _load_predictor()
    app.state.predictor_ready = app.state.predictor is not None

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "predictor_ready": app.state.predictor_ready}

    @app.get("/api/v1/models", response_model=ModelsResponse)
    def list_models() -> ModelsResponse:
        store: ProvenanceStore = app.state.store
        registered = {m["name"] for m in store.list_models()}
        models: list[dict[str, Any]] = []
        p: BaselinePredictor | None = app.state.predictor
        if p is not None:
            models.append({
                "name": "baseline",
                "version": p.version,
                "status": "registered" if "baseline" in registered else "loaded",
                "dataset_version": p.dataset_version,
                "property": p.property_name,
                "created_at": "artifact-lazy",
            })
        return ModelsResponse(models=models)

    @app.post("/api/v1/predict", response_model=PredictResponse)
    async def predict(req: PredictRequest) -> PredictResponse:
        if not app.state.predictor_ready or app.state.predictor is None:
            raise HTTPException(status_code=503, detail="Model not available. Run `python -m ml.train` first.")
        p: BaselinePredictor = app.state.predictor
        try:
            value = p.predict(req.smiles)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=f"Invalid SMILES: {exc}")
        store: ProvenanceStore = app.state.store
        trace_id = store.append_prediction({
            "model_name": "baseline",
            "model_version": p.version,
            "dataset_version": p.dataset_version,
            "input_smiles": req.smiles,
            "property": req.property,
            "output": {"property": req.property, "value": round(value, 4), "confidence": p.confidence()},
        })
        return PredictResponse(
            trace_id=trace_id,
            model_name="baseline",
            model_version=p.version,
            dataset_version=p.dataset_version,
            input_smiles=req.smiles,
            output={"property": req.property, "value": round(value, 4), "confidence": p.confidence()},
            disclaimer=DISCLAIMER,
        )

    @app.post("/api/v1/validate", response_model=ValidateResponse)
    async def validate() -> ValidateResponse:
        if not app.state.predictor_ready or app.state.predictor is None:
            raise HTTPException(status_code=503, detail="Model not available. Run `python -m ml.train` first.")
        p: BaselinePredictor = app.state.predictor
        report = run_validation(p)
        store: ProvenanceStore = app.state.store
        store.append_validation(report.to_dict())
        return ValidateResponse(report=report.to_dict(), disclaimer=DISCLAIMER)

    @app.get("/api/v1/traces/{trace_id}", response_model=TraceResponse)
    async def get_trace(trace_id: str) -> TraceResponse:
        store: ProvenanceStore = app.state.store
        rec = store.get_trace(trace_id)
        if rec is None:
            raise HTTPException(status_code=404, detail="Trace not found.")
        return TraceResponse(trace=rec)

    # Serve static dashboard. Root -> index.html.
    web_dir = WEB_DIR
    if web_dir.exists():
        app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")

        @app.get("/", include_in_schema=False)
        def index() -> FileResponse:
            return FileResponse(str(web_dir / "index.html"))

    return app


app = create_app()