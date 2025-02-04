import logging
from typing import Iterable

from aiogram import Bot

from ..validation.schemas import UnknownTypeFrameDTO
from .interface import ITelegramStrategy


_logger = logging.getLogger(__name__)


class UnknownTypeFrameTelegramStrategy(ITelegramStrategy):

    async def execute(
        self, dto: UnknownTypeFrameDTO, able_users_id: Iterable[int], bot: Bot
    ) -> dict:
        _logger.debug("Start, dto = %s", dto)
        text = (
            f"<b>НЕИЗВЕСТНЫЙ ПАКЕТ ОТ ВЕБСОКЕТ СЕРВЕРА</b> | Время: {dto.time}\n\n"
            f"Пакет: {dto.type_frame}\n"
        )
        for user_id in able_users_id:
            await bot.send_message(chat_id=user_id, text=text)
        return {}
