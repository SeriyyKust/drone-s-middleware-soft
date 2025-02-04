import logging
from abc import abstractmethod
from typing import Iterable

from aiogram import Bot
from pydantic import BaseModel

from ..validation.schemas import (
    BlockNotificationDTO,
    ErrorBlockNotificationDTO,
    GeneralNotificationDTO,
)
from .interface import ITelegramStrategy


_logger = logging.getLogger(__name__)


class AbstractNotificationTelegramStrategy(ITelegramStrategy):

    @abstractmethod
    def _get_text_notification(self, dto: BaseModel): ...

    async def execute(
        self, dto: BaseModel, able_users_id: Iterable[int], bot: Bot
    ) -> dict:
        _logger.debug("Start, dto = %s", dto)
        text = self._get_text_notification(dto)
        _logger.debug("Сформированный текст = %s", text)
        for user_id in able_users_id:
            await bot.send_message(chat_id=user_id, text=text)
        return {}


class BlockNotificationTelegramStrategy(AbstractNotificationTelegramStrategy):

    def _get_text_notification(self, dto: BlockNotificationDTO) -> str:
        return (
            f"<b>УВЕДОМЛЕНИЕ О БЛОКЕ</b> | Время: {dto.time}\n\n"
            f"Блок: {dto.data.type_block_title}\n"
            f"{dto.data.text}\n\n"
            f"Включено текстовое уведомление: "
            f"{'Да' if dto.data.enable_text_notifications else 'Нет'}\n"
            f"Включено звуковое уведомление: "
            f"{'Да' if dto.data.enable_sound_notifications else 'Нет'}"
        )


class ErrorBlockNotificationTelegramStrategy(AbstractNotificationTelegramStrategy):

    def _get_text_notification(self, dto: ErrorBlockNotificationDTO) -> str:
        return (
            f"<b>УВЕДОМЛЕНИЕ ОБ ОШИБКЕ</b> | Время: {dto.time}\n\n"
            f"Блок: {dto.data.type_block_title}\n"
            f"{dto.data.text}\n\n"
            f"Включено текстовое уведомление: "
            f"{'Да' if dto.data.enable_text_notifications else 'Нет'}\n"
            f"Включено звуковое уведомление: "
            f"{'Да' if dto.data.enable_sound_notifications else 'Нет'}"
        )


class GeneralNotificationTelegramStrategy(AbstractNotificationTelegramStrategy):

    def _get_text_notification(self, dto: GeneralNotificationDTO):
        return f"<b>ОБЩЕЕ УВЕДОМЛЕНИЕ</b> | Время: {dto.time}\n\n{dto.data.text}"
