from fastapi import Header
from fastapi.exceptions import HTTPException

from src.core.settings import app_config


async def verify_websocket_api_key(
    api_key: str = Header(alias="WS-API-Key", default=None)
):
    if api_key is None:
        raise HTTPException(status_code=401, detail="Не указан ключ авторизации")
    if api_key != app_config.webserver_api_key:
        raise HTTPException(status_code=403, detail="Неверный ключ авторизации")
    return api_key
