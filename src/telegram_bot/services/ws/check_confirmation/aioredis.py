import asyncio
import logging

from redis import asyncio as aioredis

from src.core.settings import app_config
from src.telegram_bot.services.ws.check_confirmation import ICheckConfirmation


_logger = logging.getLogger(__name__)


class AioredisCheckConfirmation(ICheckConfirmation):

    _instance = None
    _lock = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._lock = asyncio.Lock()
        return cls._instance

    @staticmethod
    async def _get_redis_connection():
        return await aioredis.from_url(app_config.redis_url)

    async def get(self, confirm_uuid: str) -> bool | None:
        _logger.debug("Start, confirm_uuid = %s", confirm_uuid)
        confirm_uuid = "test_aioredis_check_confirm" + confirm_uuid
        async with self._lock:
            redis_conn = await self._get_redis_connection()
            get_value = await redis_conn.get(confirm_uuid)
            if get_value is None:
                return None
            _logger.debug("Получены данные = %s", get_value)
            return get_value == b"True"

    async def set(self, confirm_uuid: str, confirm: bool) -> None:
        _logger.debug("Start, confirm_uuid = %s  confirm = %s", confirm_uuid, confirm)
        confirm_uuid = "test_aioredis_check_confirm" + confirm_uuid
        async with self._lock:
            redis_conn = await self._get_redis_connection()
            await redis_conn.set(confirm_uuid, str(confirm))
