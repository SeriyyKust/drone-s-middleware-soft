import logging

from aiogram.types import Update
from fastapi import APIRouter, Request

from .main import bot, dp


_logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/telegram/test/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    _logger.debug("Получены данные от веб-хука телеграмм= %S", update)
    await dp.feed_update(bot, update)
    _logger.debug("Данные полученные от веб-хука обработаны")
