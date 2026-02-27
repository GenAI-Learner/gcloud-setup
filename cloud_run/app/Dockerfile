FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr (better for Cloud Run logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Cloud Run injects the PORT env var (default 8080)
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 0 main:app
