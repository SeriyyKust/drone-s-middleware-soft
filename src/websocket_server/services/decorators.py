from abc import abstractmethod

from aiogram import Bot

from src.telegram_bot.main import bot
from src.telegram_bot.services.users import IManagerTelegramUsers
from src.telegram_bot.services.users.database import DatabaseManagerTelegramUsers
from src.websocket_server.services.ws_handler.interface import IWsServerReceiveHandler
from src.websocket_server.services.ws_handler.main_ws_server_receive_handler import (
    WsServerReceiveHandler,
)


class WsServerReceiveHandlerDecorator(IWsServerReceiveHandler):

    def __init__(self, receive_handler: WsServerReceiveHandler):
        self._receive_handler: WsServerReceiveHandler = receive_handler

    @abstractmethod
    async def execute(self, data: dict) -> dict: ...


class TelegramNotificationWsServerReceiveHandlerDecorator(
    WsServerReceiveHandlerDecorator
):

    def __init__(self, receive_handler: WsServerReceiveHandler):
        super().__init__(receive_handler)
        self._bot: Bot = bot
        self._users_manager: IManagerTelegramUsers = DatabaseManagerTelegramUsers()

    async def _send_notification_to_telegram(self, text: str):
        for user_id in await self._users_manager.get_able_users_id():
            await self._bot.send_message(chat_id=user_id, text=text)

    async def execute(self, data: dict) -> dict:
        received_data = data
        result_data = await self._receive_handler.execute(data)
        text = (
            f"ПОЛУЧЕННЫЕ ДАННЫЕ ДЛЯ ВЫПОЛНЕНИЯ:\n{received_data}\n\n"
            f"ВЫПОЛНЕННЫЕ ДЕЙСТВИЯ:\n"
            f"{str(result_data) if len(result_data) > 0 else 'НЕТ'}"
        )
        await self._send_notification_to_telegram(text)
        return result_data
