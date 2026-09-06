FROM python:3.13-slim

WORKDIR /dde
COPY product/drug-discovery-engine /dde
RUN pip install --no-cache-dir -r requirements.txt

# Train the demo artifact at image build time so the API works out of the box.
RUN python -m ml.train

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]