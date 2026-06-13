from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


class LocalStorageService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.root = Path(self.settings.local_storage_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile, folder: str = "datasets") -> str:
        suffix = Path(file.filename or "upload.h5ad").suffix
        target_dir = self.root / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{uuid4().hex}{suffix}"

        with target.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        return str(target)
