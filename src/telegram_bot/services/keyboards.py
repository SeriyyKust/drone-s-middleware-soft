from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


ABLE_TEXT = "Участвовать в процессе"
DISABLE_TEXT = "Отказаться от участия"


def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=ABLE_TEXT)
    keyboard.button(text=DISABLE_TEXT)
    return keyboard.as_markup(resize_keyboard=True)


def confirm_keyboard(custom_uuid: str) -> InlineKeyboardMarkup:
    inline_kb = [
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data=f"confirm_{custom_uuid}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Отказаться", callback_data=f"non_confirm_{custom_uuid}"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)
