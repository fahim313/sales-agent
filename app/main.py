from fastapi import Depends, FastAPI

from app.core.config import Settings, get_settings


app = FastAPI(title=get_settings().APP_NAME)


@app.get("/health")
async def health(
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    return {"status": "ok", "app": settings.APP_NAME}