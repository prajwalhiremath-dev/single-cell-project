from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExperimentCreate(BaseModel):
    dataset_id: int
    name: str
    task_type: str = Field(examples=["cell_type_annotation"])
    model_name: str = Field(examples=["geneformer", "scgpt", "scvi"])
    config: dict[str, Any] = Field(default_factory=dict)


class ExperimentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    name: str
    task_type: str
    model_name: str
    status: str
    config: dict[str, Any]
    metrics: dict[str, Any] | None = None
    artifacts: dict[str, Any] | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
