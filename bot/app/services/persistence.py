from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from bot.app.core.config import get_settings
from bot.app.services.runtime_registry import RUNTIMES, RuntimeProject
from bot.app.services.user_store import ADMINS, USERS, UserProfile

DATE_KEYS = {"created_at", "premium_until", "last_started_at"}


def _state_path() -> Path:
    root = Path(get_settings().upload_root)
    root.mkdir(parents=True, exist_ok=True)
    return root / "bot_state.json"


def _serialize_dt(v):
    return v.isoformat() if isinstance(v, datetime) else v


def save_state() -> None:
    data = {
        "users": {str(uid): {k: _serialize_dt(v) if k in DATE_KEYS else (list(v) if isinstance(v, set) else v) for k, v in asdict(profile).items()} for uid, profile in USERS.items()},
        "admins": sorted(ADMINS),
        "runtimes": {
            key: {k: _serialize_dt(v) if k in DATE_KEYS else v for k, v in asdict(r).items()}
            for key, r in RUNTIMES.items()
        },
    }
    _state_path().write_text(json.dumps(data, indent=2))


def _parse_dt(v):
    return datetime.fromisoformat(v) if isinstance(v, str) and v else None


def load_state() -> None:
    p = _state_path()
    if not p.exists():
        return
    data = json.loads(p.read_text())

    USERS.clear()
    for uid, raw in data.get("users", {}).items():
        USERS[int(uid)] = UserProfile(
            user_id=int(raw["user_id"]),
            is_banned=raw.get("is_banned", False),
            start_media_type=raw.get("start_media_type"),
            start_media_file_id=raw.get("start_media_file_id"),
            projects=set(raw.get("projects", [])),
            repos=set(raw.get("repos", [])),
            premium_until=_parse_dt(raw.get("premium_until")),
            created_at=_parse_dt(raw.get("created_at")) or datetime.utcnow(),
        )

    ADMINS.clear()
    ADMINS.update(set(data.get("admins", [])))

    RUNTIMES.clear()
    for key, raw in data.get("runtimes", {}).items():
        RUNTIMES[key] = RuntimeProject(
            key=raw["key"],
            owner_id=raw["owner_id"],
            path=raw["path"],
            run_cmd=raw["run_cmd"],
            status=raw.get("status", "stopped"),
            last_started_at=_parse_dt(raw.get("last_started_at")),
        )
