from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentRead
from app.workers.tasks import run_experiment_task

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
def create_experiment(payload: ExperimentCreate, db: Session = Depends(get_db)) -> Experiment:
    dataset = db.get(Dataset, payload.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    experiment = Experiment(
        dataset_id=payload.dataset_id,
        name=payload.name,
        task_type=payload.task_type,
        model_name=payload.model_name,
        config=payload.config,
        status="queued",
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    run_experiment_task.delay(experiment.id)
    return experiment


@router.get("/{experiment_id}", response_model=ExperimentRead)
def get_experiment(experiment_id: int, db: Session = Depends(get_db)) -> Experiment:
    experiment = db.get(Experiment, experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment
