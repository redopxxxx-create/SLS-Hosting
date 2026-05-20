from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.app.core.config import get_settings
from bot.app.services.runtime_registry import RUNTIMES, running_projects
from bot.app.services.user_store import (
    ADMINS,
    USERS,
    add_admin,
    clear_premium,
    list_admins,
    remove_admin,
    set_premium_days,
)
from bot.app.ui.layouts import card

router = Router()


def _is_admin(uid: int) -> bool:
    s = get_settings()
    return uid == s.bot_owner_id or uid in s.admin_id_list or uid in ADMINS


def _is_owner(uid: int) -> bool:
    return uid == get_settings().bot_owner_id


@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    total_users = len(USERS)
    premium_users = sum(1 for u in USERS.values() if u.is_premium)
    running = len(running_projects())
    await message.answer(card("📊 OWNER STATUS", f"👥 Users: {total_users}\n💎 Premium: {premium_users}\n🚀 Running: {running}\n📦 Projects: {len(RUNTIMES)}"))


@router.message(Command("addadmin"))
async def add_admin_handler(message: Message) -> None:
    if not _is_owner(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Usage: /addadmin <user_id>")
        return
    uid = int(parts[1])
    add_admin(uid)
    await message.answer(card("🛡 ADMIN ADDED", f"Admin ID: {uid}"))


@router.message(Command("removeadmin"))
async def remove_admin_handler(message: Message) -> None:
    if not _is_owner(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Usage: /removeadmin <user_id>")
        return
    uid = int(parts[1])
    remove_admin(uid)
    await message.answer(card("🧹 ADMIN REMOVED", f"Admin ID: {uid}"))


@router.message(Command("admins"))
async def list_admins_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await message.answer(card("🛡 ADMIN LIST", "\n".join(map(str, list_admins())) or "No dynamic admins"))


@router.message(Command("premium"))
async def premium_handler(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) < 4:
        await message.answer("Usage: /premium <user_id> <month|year|off> <count>")
        return
    user_id = int(parts[1])
    mode = parts[2].lower()
    if mode == "off":
        user = clear_premium(user_id)
        await message.answer(card("💎 PREMIUM UPDATED", f"User: {user.user_id}\nPremium: OFF"))
        return
    count = int(parts[3])
    days = 30 * count if mode == "month" else 365 * count
    user = set_premium_days(user_id, days)
    exp = user.premium_until.strftime("%Y-%m-%d") if user.premium_until else "-"
    await message.answer(card("💎 PREMIUM UPDATED", f"User: {user.user_id}\nValid Until: {exp}\nNow: {datetime.utcnow().date()}"))


@router.message(Command("setstartimage"))
async def set_start_image(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.answer("Reply to a photo with /setstartimage")
        return
    file_id = message.reply_to_message.photo[-1].file_id
    from bot.app.services.user_store import set_start_media

    set_start_media(0, "photo", file_id)
    await message.answer("Start image set.")


@router.message(Command("setstartvideo"))
async def set_start_video(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.answer("Reply to a video with /setstartvideo")
        return
    file_id = message.reply_to_message.video.file_id
    from bot.app.services.user_store import set_start_media

    set_start_media(0, "video", file_id)
    await message.answer("Start video set.")
