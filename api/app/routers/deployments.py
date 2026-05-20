from datetime import datetime
from fastapi import APIRouter

from api.app.schemas.deployment import DeploymentOut, RepoDeployRequest

router = APIRouter(prefix="/deployments", tags=["deployments"])
DEPLOYS: dict[str, dict] = {}


@router.post("/repo", response_model=DeploymentOut)
async def deploy_from_repo(payload: RepoDeployRequest) -> DeploymentOut:
    did = f"dep_{len(DEPLOYS) + 1:06d}"
    framework = []
    if "next" in payload.repo_url.lower():
        framework = ["nextjs"]
    data = {
        "id": did,
        "repo_url": payload.repo_url,
        "branch": payload.branch,
        "status": "scanning",
        "created_at": datetime.utcnow(),
        "detected_runtime": "python" if payload.repo_url.endswith(".py") else "node",
        "detected_framework": framework,
    }
    DEPLOYS[did] = data
    return DeploymentOut(**data)


@router.post("/webhook/github")
async def github_webhook(payload: dict) -> dict:
    repo = payload.get("repository", {}).get("full_name", "unknown")
    ref = payload.get("ref", "")
    return {"ok": True, "event": "push", "repo": repo, "ref": ref, "action": "auto-redeploy-queued"}
