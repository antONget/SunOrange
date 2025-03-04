from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from filter.filter import validate_russian_phone_number
import logging


def keyboards_get_contact() -> ReplyKeyboardMarkup:
    logging.info("keyboards_get_contact")
    button_1 = KeyboardButton(text='Отправить свой контакт ☎️',
                              request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1]],
        resize_keyboard=True
    )
    return keyboard


async def request_contact(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем лицевой счет
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_personal_account: {message.chat.id}')
    await message.answer(text=f'Укажите ваш номер телефона, можете воспользоваться кнопкой'
                              f' "Поделиться ☎️" расположенной ниже 👇',
                         reply_markup=keyboards_get_contact())


async def get_phone_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем номер телефона проверяем его на валидность и заносим его в БД
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'get_phone_user: {message.chat.id}')
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
    if not validate_russian_phone_number(phone):
        await message.answer(text="Неверный формат номера, повторите ввод.")
        return
    else:
        return phone