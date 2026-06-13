from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetRead
from app.services.single_cell import validate_supported_format
from app.services.storage import LocalStorageService
from app.workers.tasks import validate_dataset_task

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)) -> Dataset:
    try:
        file_format = validate_supported_format(file.filename or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    storage = LocalStorageService()
    storage_path = await storage.save_upload(file)

    dataset = Dataset(
        name=file.filename or "uploaded-dataset",
        original_filename=file.filename or "uploaded.h5ad",
        storage_path=storage_path,
        file_format=file_format,
        status="uploaded",
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    validate_dataset_task.delay(dataset.id)
    return dataset


@router.get("/{dataset_id}", response_model=DatasetRead)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)) -> Dataset:
    dataset = db.get(Dataset, dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset
