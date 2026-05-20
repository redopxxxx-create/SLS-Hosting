from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.app.core.config import get_settings
from bot.app.ui.layouts import card

router = Router()


@router.message(Command("clonebot"))
async def clone_bot_handler(message: Message) -> None:
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /clonebot <your_bot_token>")
        return

    token = parts[1].strip()
    masked = token[:8] + "..." if len(token) > 8 else "provided"
    s = get_settings()
    await message.answer(
        card(
            "🤖 BOT CLONE READY",
            f"🔑 Token: {masked}\n"
            f"🛡 Branding: {s.powered_by_text}\n"
            f"📣 Support: {s.support_channel}\n"
            "⚙ Clone deployment queued (scaffold).",
        )
    )
