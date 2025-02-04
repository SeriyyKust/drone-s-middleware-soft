import logging
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TelegramUser


_logger = logging.getLogger(__name__)


async def get_able_users(session: AsyncSession) -> Iterable[TelegramUser]:
    result = await session.execute(select(TelegramUser).filter_by(able=True))
    return result.scalars().all()


async def _get_telegram_user(pk: str, session: AsyncSession) -> TelegramUser | None:
    result = await session.execute(select(TelegramUser).filter_by(id=pk))
    return result.scalars().first()


async def _create_telegram_user(user_id: str, able: bool, session: AsyncSession) -> None:
    session.add(TelegramUser(id=user_id, able=able))
    try:
        await session.commit()
    except IntegrityError as err:
        _logger.error("Ошибка при создании пользователя в БД", exc_info=err)
        await session.rollback()


async def set_telegram_user(user_id: int, able: bool, session: AsyncSession) -> None:
    telegram_user = await _get_telegram_user(str(user_id), session)
    if telegram_user is None:
        await _create_telegram_user(user_id=str(user_id), able=able, session=session)
    else:
        telegram_user.able = able
    try:
        await session.commit()
    except IntegrityError as err:
        _logger.error("Ошибка при создании пользователя в БД", exc_info=err)
        await session.rollback()
