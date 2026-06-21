FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pipeline/pyproject.toml pipeline/
COPY pipeline/medasset pipeline/medasset/
RUN pip install --no-cache-dir -e pipeline/

COPY pipeline/ pipeline/
COPY scripts/ scripts/
COPY data/README.md data/

CMD ["python", "-m", "medasset.cli", "ingest"]
