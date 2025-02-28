from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboard_hotel_types(hotel_types: list) -> InlineKeyboardMarkup:
    logging.info("keyboard_pass_comment")
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for hotel in hotel_types:
        buttons.append(InlineKeyboardButton(text=f'{hotel}',
                                            callback_data=f'hotel_{hotel}'))
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()


def keyboard_nutrition(nutritions: list) -> InlineKeyboardMarkup:
    logging.info("keyboard_pass_comment")
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for nutrition in nutritions:
        buttons.append(InlineKeyboardButton(text=f'{nutrition}',
                                            callback_data=f'nutrition_{nutrition}'))
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()