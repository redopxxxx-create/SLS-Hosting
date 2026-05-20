import asyncio
from pathlib import Path


PLATFORM_STARTERS = {
    "heroku": "Procfile",
    "render": "render.yaml",
    "railway": "railway.json",
    "docker": "Dockerfile",
}


def suggest_deploy_targets(scan: dict) -> list[str]:
    targets = ["vps", "docker"]
    if "procfile" in scan.get("signatures", {}):
        targets.append("heroku")
    if "render.yaml" in scan.get("signatures", {}):
        targets.append("render")
    if "railway.json" in scan.get("signatures", {}):
        targets.append("railway")
    if "app.json" in scan.get("signatures", {}):
        targets.append("heroku")
    return sorted(set(targets))


async def install_dependencies(project_root: Path, runtime: str) -> tuple[bool, str]:
    if runtime == "python" and (project_root / "requirements.txt").exists():
        cmd = f"python -m pip install -r {project_root / 'requirements.txt'}"
    elif runtime == "node" and (project_root / "package.json").exists():
        cmd = "npm install"
    else:
        return True, "No dependencies detected."

    proc = await asyncio.create_subprocess_shell(
        cmd,
        cwd=str(project_root),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    out, _ = await proc.communicate()
    return proc.returncode == 0, out.decode(errors="ignore")
