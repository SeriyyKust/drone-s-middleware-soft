import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from src.exceptions import ErrorConnectWsClient
from src.telegram_bot.services.keyboards import main_keyboard, DISABLE_TEXT, ABLE_TEXT
from src.telegram_bot.services.users.database import DatabaseManagerTelegramUsers
from src.telegram_bot.services.ws.check_confirmation.aioredis import (
    AioredisCheckConfirmation,
)
from src.telegram_bot.services.ws_client import ConfirmationNotificationClient


handler_router = Router()


@handler_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Команда /start"""
    users_manager = DatabaseManagerTelegramUsers()
    await users_manager.set_able_user(message.from_user.id)
    await message.answer(
        text="Вы успешно добавлены в приложение", reply_markup=main_keyboard()
    )


@handler_router.message(F.text == DISABLE_TEXT)
async def cmd_disable_user(message: Message) -> None:
    """Команда Отказаться от участия"""
    users_manager = DatabaseManagerTelegramUsers()
    await users_manager.set_disable_user(message.from_user.id)
    await message.answer(
        text="Вы больше не участвуете в приложении", reply_markup=main_keyboard()
    )


@handler_router.message(F.text.startswith("websocket client connect: "))
async def cmd_confirmation_client(message: Message) -> None:
    url = message.text.replace("websocket client connect: ", "")
    try:
        executor = ConfirmationNotificationClient(
            url=url, bot=message.bot, users_manager=DatabaseManagerTelegramUsers()
        )
    except ErrorConnectWsClient as er:
        await message.answer(
            text=f"Не удалось подключиться к веб-сокет серверу.\nОшибка: {er}"
        )
    else:
        asyncio.create_task(executor.execute())


@handler_router.message(F.text == ABLE_TEXT)
async def cmd_able_user(message: Message) -> None:
    """Команда Участвовать в процессе"""
    users_manager = DatabaseManagerTelegramUsers()
    await users_manager.set_able_user(message.from_user.id)
    await message.answer(text="Вы участвуете в приложении", reply_markup=main_keyboard())


@handler_router.callback_query(F.data.startswith("confirm_"))
async def cmd_confirm(callback: CallbackQuery):
    confirm_uuid: str = callback.data.replace("confirm_", "")
    check = AioredisCheckConfirmation()
    await check.set(confirm_uuid, True)
    await callback.message.answer("CONFIRM YES")


@handler_router.callback_query(F.data.startswith("non_confirm_"))
async def cmd_non_confirm(callback: CallbackQuery):
    confirm_uuid: str = callback.data.replace("non_confirm_", "")
    check = AioredisCheckConfirmation()
    await check.set(confirm_uuid, False)
    await callback.message.answer("CONFIRM NO")
