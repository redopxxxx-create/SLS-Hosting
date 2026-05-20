from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class UserProfile:
    user_id: int
    is_banned: bool = False
    start_media_type: str | None = None
    start_media_file_id: str | None = None
    projects: set[str] = field(default_factory=set)
    repos: set[str] = field(default_factory=set)
    premium_until: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_premium(self) -> bool:
        return bool(self.premium_until and self.premium_until > datetime.utcnow())


USERS: dict[int, UserProfile] = {}
ADMINS: set[int] = set()


def _save() -> None:
    from bot.app.services.persistence import save_state

    save_state()


def get_or_create_user(user_id: int) -> UserProfile:
    if user_id not in USERS:
        USERS[user_id] = UserProfile(user_id=user_id)
        _save()
    return USERS[user_id]


def add_admin(user_id: int) -> None:
    ADMINS.add(user_id)
    _save()


def remove_admin(user_id: int) -> None:
    ADMINS.discard(user_id)
    _save()


def list_admins() -> list[int]:
    return sorted(ADMINS)


def set_premium_days(user_id: int, days: int) -> UserProfile:
    user = get_or_create_user(user_id)
    base = user.premium_until if user.premium_until and user.premium_until > datetime.utcnow() else datetime.utcnow()
    user.premium_until = base + timedelta(days=days)
    _save()
    return user


def clear_premium(user_id: int) -> UserProfile:
    user = get_or_create_user(user_id)
    user.premium_until = None
    _save()
    return user


def set_start_media(user_id: int, media_type: str, file_id: str) -> UserProfile:
    user = get_or_create_user(user_id)
    user.start_media_type = media_type
    user.start_media_file_id = file_id
    _save()
    return user


def can_create_more(user_id: int, max_free: int = 2) -> tuple[bool, str]:
    user = get_or_create_user(user_id)
    total = len(user.projects) + len(user.repos)
    if user.is_premium:
        return True, "premium"
    if total >= max_free:
        return False, f"Free plan limit reached ({max_free}). Upgrade to premium."
    return True, "free"
