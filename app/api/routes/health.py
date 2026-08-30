"""GET /health"""

from fastapi import APIRouter, Depends

from app.api.deps import get_settings_dep
from app.config.settings import Settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: Settings = Depends(get_settings_dep)) -> dict:
    return {
        "status": "ok",
        "app_env": settings.app_env,
        "llm_provider": settings.llm.provider,
    }
