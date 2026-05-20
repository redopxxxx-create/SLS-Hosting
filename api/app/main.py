from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.app.routers.deployments import router as deployments_router
from api.app.routers.projects import router as projects_router
from api.app.routers.system import router as system_router

app = FastAPI(title="SLS Hosting API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(deployments_router)
app.include_router(system_router)


@app.get("/")
async def root() -> dict:
    return {"ok": True, "name": "SLS Hosting API"}
