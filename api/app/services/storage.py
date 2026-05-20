from pathlib import Path

from api.app.core.config import get_settings


def ensure_user_dir(user_id: int) -> Path:
    root = Path(get_settings().upload_root)
    path = root / str(user_id)
    path.mkdir(parents=True, exist_ok=True)
    return path
