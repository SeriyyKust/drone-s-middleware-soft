import logging

from aiogram import Bot

from src.static_schemas import TypeFrame
from src.telegram_bot.services.users import IManagerTelegramUsers
from src.telegram_bot.services.ws.telegram_executor import (
    BlockNotificationWsTelegramExecutor,
    ConfirmationWsTelegramExecutor,
    ErrorBlockNotificationWsTelegramExecutor,
    GeneralNotificationWsTelegramExecutor,
    UnknownTypeFrameWsTelegramExecutor,
    WSTelegramExecutor,
)


_logger = logging.getLogger(__name__)


class WSTelegramHandler:

    def __init__(self, bot: Bot, users_manager: IManagerTelegramUsers):
        self._bot: Bot = bot
        self._users_manager = users_manager

    @classmethod
    def _create_executor(cls, type_frame: str) -> WSTelegramExecutor:
        if type_frame == TypeFrame.CONFIRMATION.value:
            return ConfirmationWsTelegramExecutor()
        elif type_frame == TypeFrame.GENERAL_NOTIFICATION.value:
            return GeneralNotificationWsTelegramExecutor()
        elif type_frame == TypeFrame.BLOCK_NOTIFICATION.value:
            return BlockNotificationWsTelegramExecutor()
        elif type_frame == TypeFrame.ERROR_BLOCK_NOTIFICATION.value:
            return ErrorBlockNotificationWsTelegramExecutor()
        else:
            return UnknownTypeFrameWsTelegramExecutor()

    @classmethod
    def _get_type_frame(cls, data: dict) -> str | None:
        _logger.debug("Start, data = %s", data)
        if "type_frame" in data:
            if isinstance(data["type_frame"], str):
                return data["type_frame"]
            else:
                _logger.warning("type_frame имеет тип %s", type(data["type_frame"]))
        else:
            logging.warning("type_frame отсутствует в data")
        return None

    async def execute(self, data: dict) -> dict:
        _logger.debug("Start, data = %s", data)
        type_frame = self._get_type_frame(data)
        if type_frame is not None:
            executor: WSTelegramExecutor = self._create_executor(type_frame)
            try:
                model = executor.validate(data)
                response_data = await executor.execute(
                    dto=model,
                    able_users_id=await self._users_manager.get_able_users_id(),
                    bot=self._bot,
                )
            except Exception as err:
                _logger.warning(
                    "Ошибка во время обработки пакета от сервера", exc_info=err
                )
            else:
                return response_data
        return {}
