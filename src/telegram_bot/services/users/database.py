import asyncio
import logging
from typing import Iterable

from src.database import new_session
from src.telegram_bot.database import calls
from src.telegram_bot.database.models import TelegramUser

from .interface import IManagerTelegramUsers


_logger = logging.getLogger(__name__)


class DatabaseManagerTelegramUsers(IManagerTelegramUsers):

    _instance = None
    _lock = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._lock = asyncio.Lock()
        return cls._instance

    async def get_able_users_id(self) -> Iterable[int]:
        async with self._lock:
            async with new_session() as session:
                able_telegram_users: Iterable[TelegramUser] = await calls.get_able_users(
                    session
                )
        return map(lambda x: int(x.id), able_telegram_users)

    async def set_able_user(self, user_id: int) -> None:
        _logger.debug("Start, user_id = %s", user_id)
        async with self._lock:
            async with new_session() as session:
                await calls.set_telegram_user(user_id=user_id, able=True, session=session)

    async def set_disable_user(self, user_id: int) -> None:
        _logger.debug("Start, user_id = %s", user_id)
        async with self._lock:
            async with new_session() as session:
                await calls.set_telegram_user(
                    user_id=user_id, able=False, session=session
                )
