"""
Internationalization Messages
"""

from typing import Dict, Literal

Language = Literal["en", "ru"]


class Messages:
    """Multi-language message system"""
    
    _messages: Dict[Language, Dict[str, str]] = {
        "en": {
            # Commands
            "cmd_start": "Start using SLS Hosting",
            "cmd_help": "Show help information",
            "cmd_projects": "View your projects",
            "cmd_status": "System status",
            "cmd_upload": "Upload new project",
            
            # Buttons
            "btn_my_projects": "📂 My Projects",
            "btn_upload_files": "📤 Upload Files",
            "btn_dashboard": "🌐 Dashboard",
            "btn_status": "📊 Status",
            "btn_settings": "⚙️ Settings",
            "btn_support": "🆘 Support",
            "btn_back": "⬅️ Back",
            
            # Welcome
            "welcome_title": "⚡ WELCOME TO SLS HOSTING ⚡",
            "welcome_desc": "Host your Telegram bots easily.\n📦 Upload ZIP/PY files instantly.\n⚡ Fast deployment system.\n🌐 Free hosting with dashboard access.",
            "welcome_verify": "Please verify by joining our channel",
            
            # Projects
            "project_empty": "You have no projects yet!",
            "project_created": "✅ Project created successfully!",
            "project_deleted": "✅ Project deleted!",
            "project_started": "▶️ Project started!",
            "project_stopped": "⏹️ Project stopped!",
            "project_restarted": "🔄 Project restarted!",
            
            # Upload
            "upload_send_file": "Send your project file (.py, .zip, .js)",
            "upload_scanning": "🔍 Scanning dependencies...",
            "upload_installing": "📦 Installing packages...",
            "upload_deploying": "🚀 Deploying project...",
            "upload_success": "✅ Project deployed successfully!",
            "upload_failed": "❌ Upload failed: {error}",
            
            # Errors
            "error_invalid_file": "❌ Invalid file format",
            "error_file_too_large": "❌ File too large (max 512MB)",
            "error_project_running": "❌ Project is already running",
            "error_insufficient_permissions": "❌ You don't have permission for this action",
            
            # Status
            "status_online": "🟢 Online",
            "status_offline": "🔴 Offline",
            "status_idle": "🟡 Idle",
        },
        "ru": {
            # Commands
            "cmd_start": "Начать использовать SLS Hosting",
            "cmd_help": "Показать справку",
            "cmd_projects": "Просмотреть проекты",
            "cmd_status": "Статус системы",
            "cmd_upload": "Загрузить проект",
            
            # Buttons
            "btn_my_projects": "📂 Мои Проекты",
            "btn_upload_files": "📤 Загрузить",
            "btn_dashboard": "🌐 Панель",
            "btn_status": "📊 Статус",
            "btn_settings": "⚙️ Параметры",
            "btn_support": "🆘 Поддержка",
            "btn_back": "⬅️ Назад",
            
            # Welcome
            "welcome_title": "⚡ ДОБРО ПОЖАЛОВАТЬ В SLS HOSTING ⚡",
            "welcome_desc": "Размещайте Telegram ботов легко.\n📦 Загружайте ZIP/PY файлы мгновенно.\n⚡ Быстрая система развертывания.\n🌐 Бесплатный хостинг с доступом к панели.",
            "welcome_verify": "Присоединитесь к нашему каналу для верификации",
            
            # Projects
            "project_empty": "У вас еще нет проектов!",
            "project_created": "✅ Проект успешно создан!",
            "project_deleted": "✅ Проект удален!",
            "project_started": "▶️ Проект запущен!",
            "project_stopped": "⏹️ Проект остановлен!",
            "project_restarted": "🔄 Проект перезагружен!",
            
            # Upload
            "upload_send_file": "Отправьте файл проекта (.py, .zip, .js)",
            "upload_scanning": "🔍 Сканирование зависимостей...",
            "upload_installing": "📦 Установка пакетов...",
            "upload_deploying": "🚀 Развертывание проекта...",
            "upload_success": "✅ Проект успешно развернут!",
            "upload_failed": "❌ Ошибка загрузки: {error}",
            
            # Errors
            "error_invalid_file": "❌ Неверный формат файла",
            "error_file_too_large": "❌ Файл слишком большой (макс 512MB)",
            "error_project_running": "❌ Проект уже запущен",
            "error_insufficient_permissions": "❌ У вас нет прав для этого действия",
            
            # Status
            "status_online": "🟢 В сети",
            "status_offline": "🔴 Оффлайн",
            "status_idle": "🟡 Ожидание",
        },
    }
    
    @classmethod
    def get(cls, key: str, language: Language = "en", **kwargs) -> str:
        """Get message by key"""
        message = cls._messages.get(language, cls._messages["en"]).get(key, key)
        if kwargs:
            return message.format(**kwargs)
        return message
    
    @classmethod
    def all(cls, language: Language = "en") -> Dict[str, str]:
        """Get all messages for language"""
        return cls._messages.get(language, cls._messages["en"])
