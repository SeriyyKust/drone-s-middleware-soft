from abc import ABC, abstractmethod
from typing import Iterable

from aiogram import Bot
from pydantic import BaseModel


class ITelegramStrategy(ABC):

    @abstractmethod
    async def execute(
        self, dto: BaseModel, able_users_id: Iterable[int], bot: Bot
    ) -> dict: ...
