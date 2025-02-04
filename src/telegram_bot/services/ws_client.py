import json
import logging

from aiogram import Bot
from websockets.asyncio.client import connect as async_connect
from websockets.sync.client import ClientConnection as SyncClientConnection
from websockets.sync.client import connect as sync_connect

from src.exceptions import ErrorConnectWsClient
from src.telegram_bot.services.users import IManagerTelegramUsers
from src.telegram_bot.services.ws_handler import WSTelegramHandler


_logger = logging.getLogger(__name__)


class ConfirmationNotificationClient:

    def __init__(self, url: str, bot: Bot, users_manager: IManagerTelegramUsers):
        self._url: str = self._validate_confirmation_data(url)
        self._bot = bot
        self._users_manager: IManagerTelegramUsers = users_manager

    @staticmethod
    def _validate_confirmation_data(url: str):
        try:
            conn: SyncClientConnection = sync_connect(url)
            conn.close()
        except Exception as er:
            raise ErrorConnectWsClient(
                f"Не удалость подключиться к серверу. Error: {er}."
            )
        else:
            return url

    async def execute(self):
        handler = WSTelegramHandler(bot=self._bot, users_manager=self._users_manager)
        try:
            async with async_connect(self._url) as websock:
                while True:
                    recv_message = await websock.recv()
                    load_recv_message: dict = json.loads(recv_message)
                    _logger.debug(
                        "Веб-сокет клиент получил сообщение = %s", load_recv_message
                    )
                    response_handler_data = await handler.execute(load_recv_message)
                    if len(response_handler_data) > 0:
                        await websock.send(json.dumps(response_handler_data))
        except Exception as er:
            _logger.warning(
                "Получена ошибка в обработке сообщений в Веб-сокет клиенте", exc_info=er
            )
