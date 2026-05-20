from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str
    runtime: str = Field(pattern="^(python|node|file)$")
    owner_id: int


class ProjectOut(BaseModel):
    id: str
    name: str
    runtime: str
    status: str
    created_at: datetime
