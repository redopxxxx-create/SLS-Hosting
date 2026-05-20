from __future__ import annotations

import asyncio
import logging

from bot.app.core.config import get_settings
from bot.app.services.runtime_registry import mark_running, running_projects


async def restart_all_projects_loop() -> None:
    settings = get_settings()
    hours = max(1, settings.restart_interval_hours)
    while True:
        await asyncio.sleep(hours * 3600)
        for p in running_projects():
            logging.info("Auto-restarting project: %s", p.key)
            mark_running(p.key)
