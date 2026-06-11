from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    original_filename: str
    storage_path: str
    file_format: str
    status: str
    summary: dict | None = None
    created_at: datetime
    updated_at: datetime


class DatasetSummary(BaseModel):
    cells: int | None = None
    genes: int | None = None
    obs_columns: list[str] = []
    var_columns: list[str] = []
    has_raw: bool = False
