from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📂 My Projects", callback_data="projects")
    kb.button(text="📤 Upload Files", callback_data="upload")
    kb.button(text="🌐 Dashboard", callback_data="dashboard")
    kb.button(text="📊 Status", callback_data="status")
    kb.button(text="⚙ Settings", callback_data="settings")
    kb.button(text="🆘 Support", callback_data="support")
    kb.adjust(2, 2, 2)
    return kb.as_markup()


def project_menu(project_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for label, action in [
        ("▶ Start", "start"),
        ("⏹ Stop", "stop"),
        ("🔄 Restart", "restart"),
        ("📜 Logs", "logs"),
        ("✏ Edit", "edit"),
        ("📂 Files", "files"),
        ("🗑 Delete", "delete"),
        ("🌐 Open Dashboard", "dash"),
    ]:
        kb.button(text=label, callback_data=f"project:{action}:{project_id}")
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()
