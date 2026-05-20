from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.app.core.config import get_settings
from bot.app.services.user_store import USERS
from bot.app.ui.layouts import card

router = Router()


def _is_admin(uid: int) -> bool:
    s = get_settings()
    return uid == s.bot_owner_id or uid in s.admin_id_list


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /broadcast <message>")
        return

    text = parts[1]
    sent = 0
    failed = 0
    for uid in USERS.keys():
        if uid == 0:
            continue
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception:
            failed += 1

    await message.answer(
        card(
            "📣 BROADCAST REPORT",
            f"✅ Sent: {sent}\n"
            f"❌ Failed: {failed}\n"
            f"👨‍💻 Dev: {get_settings().developer_name}",
        )
    )
