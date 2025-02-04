import asyncio
import logging

import redis
from fastapi import FastAPI

from src.core.settings import app_config
from src.database import Base, engine
from src.telegram_bot.main import lifespan
from src.telegram_bot.router import router as telegram_bot_router
from src.websocket_server.router import router as websocket_router


_logger = logging.getLogger(__name__)


def check_redis_connect() -> None:
    _logger.debug(
        "Проверка подключения к Redis: host = %s port = %s",
        app_config.redis_host,
        app_config.redis_port,
    )
    r = redis.Redis(host=app_config.redis_host, port=app_config.redis_port)
    try:
        response = r.ping()
        if response:
            _logger.debug("Подключение к Redis успешно")
        else:
            _logger.warning("От Redis не получен Pong")
    except Exception as e:
        _logger.warning("Не удалось подключиться к redis", exc_info=e)


async def init_models():
    async with engine.begin() as conn:
        try:
            _logger.debug("Создание таблиц в БД")
            await conn.run_sync(Base.metadata.create_all)
        except Exception as err:
            _logger.warning("Не удалось создать таблицы для БД", exc_info=err)
        else:
            _logger.debug("Таблицы в БД созданы успешно")


app = FastAPI(lifespan=lifespan)


def main(main_app: FastAPI):
    main_app.include_router(websocket_router)
    main_app.include_router(telegram_bot_router)
    check_redis_connect()
    asyncio.create_task(init_models())


main(app)
