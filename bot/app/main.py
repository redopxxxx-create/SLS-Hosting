import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.app.core.config import get_settings
from bot.app.handlers.admin import router as admin_router
from bot.app.handlers.broadcast import router as broadcast_router
from bot.app.handlers.clone import router as clone_router
from bot.app.handlers.repo import router as repo_router
from bot.app.handlers.start import router as start_router
from bot.app.services.persistence import load_state
from bot.app.services.scheduler import restart_all_projects_loop


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    load_state()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(repo_router)
    dp.include_router(clone_router)
    dp.include_router(admin_router)
    dp.include_router(broadcast_router)
    asyncio.create_task(restart_all_projects_loop())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
