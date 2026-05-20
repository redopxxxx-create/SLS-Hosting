import psutil
from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status")
async def system_status() -> dict:
    return {
        "cpu": psutil.cpu_percent(interval=0.2),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
    }
