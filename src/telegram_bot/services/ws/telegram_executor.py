from typing import Iterable

from aiogram import Bot
from pydantic import BaseModel

from src.telegram_bot.services.ws.check_confirmation.aioredis import (
    AioredisCheckConfirmation,
)
from src.telegram_bot.services.ws.strategy import ITelegramStrategy
from src.telegram_bot.services.ws.strategy.confirmation import (
    ConfirmationTelegramStrategy,
)
from src.telegram_bot.services.ws.strategy.notification import (
    BlockNotificationTelegramStrategy,
    ErrorBlockNotificationTelegramStrategy,
    GeneralNotificationTelegramStrategy,
)
from src.telegram_bot.services.ws.strategy.unknown_type_frame import (
    UnknownTypeFrameTelegramStrategy,
)
from src.telegram_bot.services.ws.validation import IValidationWSData
from src.telegram_bot.services.ws.validation.confirmation import (
    ConfirmationValidationData,
)
from src.telegram_bot.services.ws.validation.notification import (
    BlockNotificationValidationData,
    ErrorBlockNotificationValidationData,
    GeneralNotificationValidationData,
)
from src.telegram_bot.services.ws.validation.unknown_type_frame import (
    UnknownTypeFrameValidationData,
)


class WSTelegramExecutor:

    def __init__(self, validation: IValidationWSData, strategy: ITelegramStrategy):
        self._validation: IValidationWSData = validation
        self._strategy: ITelegramStrategy = strategy

    def validate(self, data: dict) -> BaseModel:
        return self._validation.validate(data)

    async def execute(
        self, dto: BaseModel, able_users_id: Iterable[int], bot: Bot
    ) -> dict:
        return await self._strategy.execute(dto=dto, able_users_id=able_users_id, bot=bot)


class GeneralNotificationWsTelegramExecutor(WSTelegramExecutor):

    def __init__(self):
        super().__init__(
            validation=GeneralNotificationValidationData(),
            strategy=GeneralNotificationTelegramStrategy(),
        )


class BlockNotificationWsTelegramExecutor(WSTelegramExecutor):

    def __init__(self):
        super().__init__(
            validation=BlockNotificationValidationData(),
            strategy=BlockNotificationTelegramStrategy(),
        )


class ErrorBlockNotificationWsTelegramExecutor(WSTelegramExecutor):

    def __init__(self):
        super().__init__(
            validation=ErrorBlockNotificationValidationData(),
            strategy=ErrorBlockNotificationTelegramStrategy(),
        )


class ConfirmationWsTelegramExecutor(WSTelegramExecutor):

    def __init__(self):
        super().__init__(
            validation=ConfirmationValidationData(),
            strategy=ConfirmationTelegramStrategy(
                check_confirmation=AioredisCheckConfirmation()
            ),
        )


class UnknownTypeFrameWsTelegramExecutor(WSTelegramExecutor):

    def __init__(self):
        super().__init__(
            validation=UnknownTypeFrameValidationData(),
            strategy=UnknownTypeFrameTelegramStrategy(),
        )
