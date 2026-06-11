# CellScape: Single-Cell Foundation Model Lab

An open-source platform to help researchers run single-cell AI experiments without manually managing preprocessing, GPU jobs, model evaluation, and result tracking.

## Problem being solved

Single-cell foundation models such as Geneformer and scGPT are powerful, but the workflow is difficult for many biology teams:

```text
Prepare AnnData files -> run QC/preprocessing -> configure GPU jobs -> run models -> evaluate -> interpret -> compare experiments
```

This project aims to make that workflow reproducible and easier to run through APIs and, later, a UI.

## Initial MVP workflow

```text
Upload .h5ad dataset
        ↓
Validate AnnData structure
        ↓
Generate dataset summary
        ↓
Create experiment record
        ↓
Queue preprocessing / model job
        ↓
Store metrics and artifacts
        ↓
Compare runs
```

## Current scaffold

- FastAPI backend
- SQLAlchemy database models
- Dataset upload API
- Experiment API
- Celery worker skeleton
- Scanpy/AnnData service skeleton
- Docker Compose with PostgreSQL, Redis, MinIO, API, worker, and MLflow
- Pytest starter tests

## Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Celery + Redis
- Scanpy / AnnData
- MLflow
- MinIO or S3-compatible storage
- Docker Compose

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open API docs:

```text
http://localhost:8000/docs
```

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## API examples

Health check:

```bash
curl http://localhost:8000/health
```

Create an experiment:

```bash
curl -X POST http://localhost:8000/api/v1/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": 1,
    "name": "geneformer-cell-type-baseline",
    "task_type": "cell_type_annotation",
    "model_name": "geneformer",
    "config": {"epochs": 3, "batch_size": 8}
  }'
```

## Roadmap

### Phase 1: Foundation

- [x] Project scaffold
- [x] FastAPI application
- [x] Dataset and experiment schemas
- [x] Database model skeleton
- [x] Worker skeleton
- [ ] Complete DB migrations with Alembic
- [ ] Persist uploaded datasets to object storage
- [ ] Add real `.h5ad` validation and summary extraction

### Phase 2: Single-cell pipeline

- [ ] Scanpy preprocessing pipeline
- [ ] QC metrics and plots
- [ ] UMAP generation
- [ ] scVI baseline

### Phase 3: Foundation models

- [ ] Geneformer adapter
- [ ] scGPT adapter
- [ ] Embedding extraction
- [ ] Classifier-head fine-tuning
- [ ] Model comparison dashboard

### Phase 4: Interpretability

- [ ] Marker gene enrichment
- [ ] Layer-wise embedding probes
- [ ] Attention/gene signal analysis
- [ ] Downloadable experiment reports

## Repository structure

```text
app/
  api/
  core/
  db/
  models/
  schemas/
  services/
  workers/
tests/
docker-compose.yml
Dockerfile
pyproject.toml
```

## Note

This is an early MVP scaffold. The next milestone is to complete an end-to-end local flow:

```text
Upload .h5ad -> validate -> summarize -> create experiment -> queue worker -> update status
```
