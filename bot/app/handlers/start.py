from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.app.core.config import get_settings
from bot.app.services.user_store import USERS, get_or_create_user
from bot.app.ui.keyboards import main_menu
from bot.app.ui.layouts import card

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    settings = get_settings()
    get_or_create_user(message.from_user.id)

    text = card(
        "⚡ WELCOME ⚡",
        "🚀 Host your Telegram bots & repos easily.\n"
        "📦 Multi files / multi repos / multi users ready.\n"
        f"🌐 Support: {settings.support_channel}\n"
        f"🛡 {settings.powered_by_text}\n"
        f"👨‍💻 Dev: {settings.developer_name}",
    )

    global_media = USERS.get(0)
    if global_media and global_media.start_media_type == "photo" and global_media.start_media_file_id:
        await message.answer_photo(global_media.start_media_file_id, caption=text, reply_markup=main_menu())
        return
    if global_media and global_media.start_media_type == "video" and global_media.start_media_file_id:
        await message.answer_video(global_media.start_media_file_id, caption=text, reply_markup=main_menu())
        return

    await message.answer(text, reply_markup=main_menu())
