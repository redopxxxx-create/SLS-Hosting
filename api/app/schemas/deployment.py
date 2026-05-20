from datetime import datetime
from pydantic import BaseModel, Field


class RepoDeployRequest(BaseModel):
    repo_url: str
    branch: str = "main"
    token: str | None = None
    preferred_platform: str | None = None


class DeploymentOut(BaseModel):
    id: str
    repo_url: str
    branch: str
    status: str = Field(default="queued")
    created_at: datetime
    detected_runtime: str | None = None
    detected_framework: list[str] = []
