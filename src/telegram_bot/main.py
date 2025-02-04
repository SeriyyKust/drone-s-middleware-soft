import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from src.core.settings import app_config
from src.telegram_bot.services.handlers import handler_router


_logger = logging.getLogger(__name__)


bot = Bot(
    token=app_config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    _logger.debug(
        "Настройка веб-хука для телеграмма: url = %s", app_config.get_webhook_url()
    )
    dp.include_router(handler_router)
    await bot.set_webhook(
        url=app_config.get_webhook_url(),
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,  # Удалить ожидающие обновления
    )
    yield
    # Код выполняется при завершении работы
    await bot.delete_webhook()
    _logger.debug("Веб-хук удалён")
