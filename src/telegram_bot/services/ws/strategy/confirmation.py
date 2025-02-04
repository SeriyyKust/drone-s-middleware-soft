import asyncio
import datetime
import logging
import time
from typing import Iterable

from aiogram import Bot

from ...keyboards import confirm_keyboard
from ..check_confirmation import ICheckConfirmation
from ..validation.schemas import ConfirmationDTO
from .interface import ITelegramStrategy


_logger = logging.getLogger(__name__)


class ConfirmationTelegramStrategy(ITelegramStrategy):

    def __init__(
        self,
        check_confirmation: ICheckConfirmation,
        cycle_sleep: int = 5,
        cycle_duration: int = 20,
    ):
        self._check_confirmation: ICheckConfirmation = check_confirmation
        self._cycle_sleep: int = cycle_sleep
        self._cycle_duration: int = cycle_duration

    async def execute(
        self, dto: ConfirmationDTO, able_users_id: Iterable[int], bot: Bot
    ) -> dict:
        _logger.debug("Start, dto = %s", dto)
        for user_id in able_users_id:
            await bot.send_message(
                chat_id=user_id,
                text=f"ПОДТВЕРЖДЕНИЕ ВЫПОДНЕНИЯ КОМАНДЫ | {dto.time}\n\n"
                f"БЛОК: {dto.data.type_block_title}\n"
                f"КОМАНДА: {dto.data.command_title}\n"
                f"ПРОДОЛЖИТЕЛЬНОСТЬ: {dto.data.duration}\n"
                f"ОЖИДАТЬ ВЫПОЛНЕНИЯ: {'Да' if dto.data.wait_to_complete else 'Нет'}",
                reply_markup=confirm_keyboard(dto.data.id),
            )
        _logger.debug(
            "Начало цикла ожидания подтверждения от телеграмм, sleep = %s  duration = %s",
            self._cycle_sleep,
            self._cycle_duration,
        )
        start_time = time.time()
        while True:
            check = await self._check_confirmation.get(confirm_uuid=dto.data.id)
            if check is None:
                await asyncio.sleep(self._cycle_sleep)
            else:
                return {
                    "time": str(datetime.datetime.now()),
                    "id": dto.data.id,
                    "confirmation": 1 if check else 2,
                }
            current_time = time.time() - start_time
            if current_time > self._cycle_duration:
                break
            _logger.debug("Прошло времени в цикле = %.5f")
        return {
            "time": str(datetime.datetime.now()),
            "id": dto.data.id,
            "confirmation": 2,
        }
