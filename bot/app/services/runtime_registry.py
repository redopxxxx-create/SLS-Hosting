from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuntimeProject:
    key: str
    owner_id: int
    path: str
    run_cmd: str
    status: str = "stopped"
    last_started_at: datetime | None = None


RUNTIMES: dict[str, RuntimeProject] = {}


def _save() -> None:
    from bot.app.services.persistence import save_state

    save_state()


def register_project(key: str, owner_id: int, path: str, run_cmd: str) -> RuntimeProject:
    project = RuntimeProject(key=key, owner_id=owner_id, path=path, run_cmd=run_cmd)
    RUNTIMES[key] = project
    _save()
    return project


def mark_running(key: str) -> None:
    if key in RUNTIMES:
        RUNTIMES[key].status = "running"
        RUNTIMES[key].last_started_at = datetime.utcnow()
        _save()


def running_projects() -> list[RuntimeProject]:
    return [p for p in RUNTIMES.values() if p.status == "running"]
