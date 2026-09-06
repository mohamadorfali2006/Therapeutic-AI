# Drug Discovery Engine — Multi-stage Docker build
# Bakes model artifacts into the image so the API works out of the box

# Stage 1: Training (produces model artifacts)
FROM python:3.13-slim AS training

WORKDIR /dde
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml/ ./ml/
COPY app/ ./app/

# Train all model artifacts at build time
RUN python -m ml.train

# Stage 2: Runtime (smaller image, no build tools)
FROM python:3.13-slim AS runtime

WORKDIR /dde

# Copy only runtime requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY ml/ ./ml/
COPY web/ ./web/

# Copy trained artifacts from training stage
COPY --from=training /dde/ml/artifacts/ ./ml/artifacts/

# Verify artifacts exist
RUN ls -la ml/artifacts/

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
