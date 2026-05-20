from pathlib import Path

SIGNATURES = {
    "requirements.txt": "python",
    "package.json": "node",
    "main.py": "python",
    "bot.py": "telegram",
    "index.js": "node",
    "server.js": "node",
    "procfile": "proc",
    "runtime.txt": "runtime",
    "dockerfile": "docker",
    "docker-compose.yml": "compose",
    "railway.json": "railway",
    "render.yaml": "render",
    "app.json": "heroku",
    "nixpacks.toml": "nixpacks",
    "manage.py": "django",
    "flask": "flask",
    "fastapi": "fastapi",
    ".env": "env",
}


FRAMEWORK_RULES = {
    "django": ["manage.py"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "express": ["server.js", "index.js"],
    "react": ["package.json"],
    "docker": ["dockerfile"],
}


def scan_project(path: Path) -> dict:
    found: dict[str, str] = {}
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        key = file.name.lower()
        if key in SIGNATURES:
            found[key] = SIGNATURES[key]

    runtime = "python" if "requirements.txt" in found or "main.py" in found else "node"
    entrypoint = "main.py" if "main.py" in found else "index.js"
    frameworks = [
        name for name, markers in FRAMEWORK_RULES.items() if any(marker in found for marker in markers)
    ]
    project_type = "telegram-bot" if "bot.py" in found else "web-app"

    return {
        "runtime": runtime,
        "entrypoint": entrypoint,
        "frameworks": frameworks,
        "project_type": project_type,
        "signatures": found,
        "platform_files": [k for k in found if k in {"procfile", "render.yaml", "railway.json", "app.json", "dockerfile", "nixpacks.toml"}],
    }
