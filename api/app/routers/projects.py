from datetime import datetime
from fastapi import APIRouter

from api.app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/projects", tags=["projects"])
PROJECTS: dict[str, dict] = {}


@router.get("", response_model=list[ProjectOut])
async def list_projects() -> list[ProjectOut]:
    return [ProjectOut(**v) for v in PROJECTS.values()]


@router.post("", response_model=ProjectOut)
async def create_project(payload: ProjectCreate) -> ProjectOut:
    pid = f"prj_{len(PROJECTS) + 1:06d}"
    data = {
        "id": pid,
        "name": payload.name,
        "runtime": payload.runtime,
        "status": "stopped",
        "created_at": datetime.utcnow(),
    }
    PROJECTS[pid] = data
    return ProjectOut(**data)
