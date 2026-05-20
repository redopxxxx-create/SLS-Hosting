from __future__ import annotations

import asyncio
from pathlib import Path

from bot.app.services.repo_providers import RepoInput


async def clone_repo(repo: RepoInput, target_dir: Path) -> tuple[bool, str]:
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        return False, f"Target already exists: {target_dir}"

    clone_url = repo.url
    if repo.token and clone_url.startswith("https://") and "@" not in clone_url:
        clone_url = clone_url.replace("https://", f"https://oauth2:{repo.token}@", 1)

    cmd = ["git", "clone", "--depth", "1", "--branch", repo.branch, clone_url, str(target_dir)]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    out, _ = await proc.communicate()
    return proc.returncode == 0, out.decode(errors="ignore")


async def pull_latest(project_dir: Path) -> tuple[bool, str]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "pull",
        cwd=str(project_dir),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    out, _ = await proc.communicate()
    return proc.returncode == 0, out.decode(errors="ignore")
