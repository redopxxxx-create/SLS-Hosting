from pathlib import Path
from time import perf_counter

from aiogram import F, Router
from aiogram.types import Message

from bot.app.core.config import get_settings
from bot.app.services.deployer import suggest_deploy_targets
from bot.app.services.repo_manager import clone_repo
from bot.app.services.repo_providers import RepoInput, detect_platform
from bot.app.services.scanner import scan_project
from bot.app.services.user_store import can_create_more, get_or_create_user
from bot.app.ui.layouts import card
from bot.app.ui.progress import progress_bar, speed_line

router = Router()


@router.message(F.text.regexp(r"https?://"))
async def handle_repo_link(message: Message) -> None:
    url = message.text.strip()
    user = get_or_create_user(message.from_user.id)
    ok_limit, reason = can_create_more(user.user_id)
    if not ok_limit:
        await message.answer(card("⚠ LIMIT REACHED", f"{reason}\nUse premium for more active repos/projects."))
        return

    platform = detect_platform(url)
    status = await message.answer(card("⏬ REPO IMPORT", "Preparing clone..."))

    settings = get_settings()
    project_dir = Path(settings.upload_root) / str(message.from_user.id) / f"repo_{len(user.repos)+1}"
    start = perf_counter()
    await status.edit_text(card("⏬ REPO IMPORT", f"{progress_bar(1,4)} 25%\nCloning repository..."))
    ok, log = await clone_repo(RepoInput(url=url), project_dir)
    if not ok:
        await status.edit_text(card("❌ CLONE FAILED", f"`{log[:1000]}`"))
        return

    await status.edit_text(card("🔎 SCAN", f"{progress_bar(2,4)} 50%\nScanning files & frameworks..."))
    scan = scan_project(project_dir)
    targets = ", ".join(suggest_deploy_targets(scan))
    elapsed = max(0.001, perf_counter() - start)
    fake_bytes = 8 * 1024 * 1024
    speed = speed_line(fake_bytes / elapsed)

    user.repos.add(project_dir.name)
    from bot.app.services.persistence import save_state
    save_state()
    await status.edit_text(card("⚙ DEPLOY PREP", f"{progress_bar(3,4)} 75%\nResolving deploy targets...\nSpeed: {speed}"))
    await status.edit_text(
        card(
            "🚀 DEPLOYMENT PANEL",
            f"{progress_bar(4,4)} 100%\n"
            f"📦 Repo: {project_dir.name}\n"
            f"🌐 Platform: {platform.value}\n"
            f"⚡ Runtime: {scan['runtime']}\n"
            f"🧠 Frameworks: {', '.join(scan['frameworks']) or 'auto'}\n"
            f"☁ Targets: {targets}\n"
            f"🔥 Status: Ready",
        )
    )
