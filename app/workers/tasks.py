from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.services.single_cell import summarize_h5ad
from app.workers.celery_app import celery_app


@celery_app.task(name="validate_dataset")
def validate_dataset_task(dataset_id: int) -> dict:
    db: Session = SessionLocal()
    dataset = db.get(Dataset, dataset_id)
    if dataset is None:
        db.close()
        return {"status": "failed", "error": "Dataset not found"}

    dataset.status = "validating"
    db.commit()

    summary = summarize_h5ad(dataset.storage_path)
    dataset.summary = summary
    dataset.status = "ready"
    db.commit()
    db.close()
    return {"status": "ready", "summary": summary}


@celery_app.task(name="run_experiment")
def run_experiment_task(experiment_id: int) -> dict:
    db: Session = SessionLocal()
    experiment = db.get(Experiment, experiment_id)
    if experiment is None:
        db.close()
        return {"status": "failed", "error": "Experiment not found"}

    experiment.status = "running"
    db.commit()

    experiment.metrics = {
        "message": "Experiment worker executed placeholder pipeline",
        "model_name": experiment.model_name,
        "task_type": experiment.task_type,
    }
    experiment.artifacts = {}
    experiment.status = "completed"
    db.commit()
    db.close()
    return {"status": "completed", "metrics": experiment.metrics}
