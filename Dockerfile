FROM python:3.11-slim

WORKDIR /app

# Optional: install build deps if any packages need compilation
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use non-root user for safety (optional)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PYTHONPATH=/app

EXPOSE 8000

# Run uvicorn; replace "src.main:app" with your module where `app = FastAPI()` lives
CMD ["uvicorn", "Incident_api:app", "--host", "0.0.0.0", "--port", "80"]