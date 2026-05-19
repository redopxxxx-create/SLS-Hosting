"""
Main Telegram Bot Entry Point
SLS Hosting - Premium File & Bot Hosting Platform
"""

import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config.settings import settings
from config.ui import UICard, Button, Emojis
from config.messages import Messages
from config.constants import APP_NAME, APP_DESCRIPTION

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize Pyrogram client
app = Client(
    name="sls_hosting_bot",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    workdir="./storage/bot_session"
)


# ============ START COMMAND ============

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command with premium UI"""
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    
    # Create welcome message
    welcome_text = f"""{UICard.header("⚡ WELCOME TO SLS HOSTING ⚡")}

{Emojis.rocket} Host your Telegram bots easily
{Emojis.package} Upload ZIP/PY files instantly
{Emojis.zap} Fast deployment system
{Emojis.globe} Free hosting with dashboard access

{UICard.separator()}

Welcome, <b>{user_name}</b>!

Start by exploring your dashboard or uploading your first project.
"""
    
    # Create keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📂 My Projects", callback_data="projects"),
                InlineKeyboardButton("📤 Upload", callback_data="upload"),
            ],
            [
                InlineKeyboardButton("🌐 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("📊 Status", callback_data="status"),
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
                InlineKeyboardButton("🆘 Support", callback_data="support"),
            ],
        ]
    )
    
    await message.reply_text(welcome_text, reply_markup=keyboard, parse_mode="HTML")
    logger.info(f"User {user_id} started the bot")


# ============ HELP COMMAND ============

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Show help information"""
    
    help_text = f"""{UICard.header("📖 HELP")}

<b>Available Commands:</b>

/start - Start the bot
/help - Show this help
/projects - View your projects
/status - System status
/upload - Upload new project

<b>Features:</b>

{Emojis.file} <b>File Hosting</b> - Upload and share files
{Emojis.robot} <b>Bot Hosting</b> - Deploy Python/Node.js bots
{Emojis.settings} <b>Management</b> - Control your projects
{Emojis.zap} <b>Fast</b> - Instant deployment
{Emojis.shield} <b>Secure</b> - Safe sandboxed execution

<b>Need more help?</b>
Contact support: /support
"""
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 Documentation", url=settings.DOCS_URL)],
            [InlineKeyboardButton("⬅️ Back", callback_data="start")],
        ]
    )
    
    await message.reply_text(help_text, reply_markup=keyboard, parse_mode="HTML")


# ============ CALLBACK HANDLERS ============

@app.on_callback_query()
async def handle_callbacks(client: Client, callback_query):
    """Handle inline button callbacks"""
    
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    # Projects callback
    if data == "projects":
        await callback_query.answer("Opening projects...", show_alert=False)
        text = f"""{UICard.header("📂 MY PROJECTS")}

You have <b>0 projects</b>

Use the upload button to create your first project!
"""
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📤 Upload Project", callback_data="upload")],
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    # Upload callback
    elif data == "upload":
        await callback_query.answer("Send your project file", show_alert=False)
        text = f"""{UICard.header("📤 UPLOAD PROJECT")}

Send your project file:
• <code>.py</code> - Python script
• <code>.zip</code> - Zipped project
• <code>.js</code> - Node.js script

Supported frameworks:
• Pyrogram, Telethon, Aiogram (Python)
• Discord.js, Telegraf (Node.js)

Maximum file size: <b>512MB</b>
"""
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    # Dashboard callback
    elif data == "dashboard":
        dashboard_url = f"{settings.DASHBOARD_URL}?user_id={user_id}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🌐 Open Dashboard", url=dashboard_url)],
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        text = f"""{UICard.header("🌐 DASHBOARD")}

Click below to access your web dashboard:
• Project management
• File explorer
• Live logs
• Performance monitoring
"""
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    # Status callback
    elif data == "status":
        text = f"""{UICard.header("📊 SYSTEM STATUS")}

{UICard.box("System", f"{Emojis.status_online} Operational")}

{UICard.box("Your Quota", "0 / 5 GB used")}

{UICard.box("Projects", "0 active / 0 total")}

{UICard.separator()}

Projects hosted: <b>0</b>
Files hosted: <b>0</b>
"""
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    # Settings callback
    elif data == "settings":
        text = f"""{UICard.header("⚙️ SETTINGS")}

<b>Language</b>
Current: English (EN)

<b>Notifications</b>
All enabled

<b>Storage</b>
0 GB / 5 GB used
"""
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🌍 Language", callback_data="language")],
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")
    
    # Support callback
    elif data == "support":
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Telegram Support", url=settings.SUPPORT_URL)],
                [InlineKeyboardButton("📧 Email Support", url=f"mailto:{settings.SUPPORT_EMAIL}")],
                [InlineKeyboardButton("⬅️ Back", callback_data="start")],
            ]
        )
        text = f"""{UICard.header("🆘 SUPPORT")}

Need help? Contact us:

{Emojis.chat} Telegram: @sls_support
{Emojis.email} Email: support@sls.local
{Emojis.globe} Website: sls.local

Response time: <b>Usually under 1 hour</b>
"""
        await callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


# ============ MESSAGE HANDLERS ============

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file_upload(client: Client, message: Message):
    """Handle file uploads"""
    
    document = message.document
    file_size_mb = document.file_size / 1024 / 1024
    
    if file_size_mb > 512:
        await message.reply_text(f"❌ File too large! Maximum 512MB, you sent {file_size_mb:.1f}MB")
        return
    
    # Show upload progress
    progress_text = f"""{UICard.header("📤 UPLOADING")}

{UICard.progress_bar(0, 100)}

File: <code>{document.file_name}</code>
Size: {file_size_mb:.1f} MB
"""
    progress_msg = await message.reply_text(progress_text, parse_mode="HTML")
    
    # Download file
    try:
        file_path = await client.download_media(message)
        
        await progress_msg.edit_text(f"""{UICard.header("📤 UPLOADING")}

{UICard.progress_bar(100, 100)}

✅ File uploaded successfully!

{UICard.separator()}

Next: Analyzing dependencies...
""", parse_mode="HTML")
        
        logger.info(f"File uploaded: {file_path}")
        
    except Exception as e:
        await progress_msg.edit_text(f"❌ Upload failed: {str(e)}", parse_mode="HTML")
        logger.error(f"Upload error: {str(e)}")


# ============ ERROR HANDLERS ============

@app.on_message()
async def default_handler(client: Client, message: Message):
    """Default message handler"""
    
    if message.text and message.text.startswith("/"):
        await message.reply_text("❓ Unknown command. Use /help for available commands.")


# ============ BOT STARTUP ============

async def main():
    """Start the bot"""
    try:
        logger.info("Starting SLS Hosting Bot...")
        logger.info(f"Bot username will be set after connecting")
        
        await app.start()
        logger.info(f"✅ Bot started successfully!")
        logger.info(f"Bot is running and listening for messages...")
        
        # Keep bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        raise
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
