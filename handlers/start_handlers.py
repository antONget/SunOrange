import logging

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup

from database import requests as rq
from config_data.config import Config, load_config
from utils.error_handling import error_handler
from utils.send_phone_contact import request_contact, get_phone_user
from utils.utils_keybords import utils_handler_pagination_and_select_item
from services.integration_u_on import method_get_countries, method_get_company_office, method_post_lead
from filter.filter import validate_date_birthday
from keyboards.start_keyboard import keyboard_hotel_types, keyboard_nutrition

config: Config = load_config()
router = Router()
router.message.filter(F.chat.type == "private")


class StateOrder(StatesGroup):
    fullname_state = State()
    country_state = State()
    city_state = State()
    data_department_state = State()
    count_night_state = State()
    count_tourist_state = State()
    age_kids_state = State()
    budget_state = State()
    phone_state = State()
    office_state = State()


@router.message(CommandStart())
@error_handler
async def start(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск бота
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('start')
    tg_id = message.chat.id
    await state.set_state(state=None)
    await state.clear()
    if message.from_user.username:
        username = message.from_user.username
    else:
        username = "Ник отсутствует"
    data = {"tg_id": tg_id, "username": username}
    await rq.add_user(tg_id=tg_id, data=data)
    await message.answer(text='Давайте познакомимся! Как вас зовут?')
    await state.set_state(StateOrder.fullname_state)


@router.message(F.text, StateFilter(StateOrder.fullname_state))
@error_handler
async def get_fullname(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_fullname')
    fullname = message.text
    await state.update_data(fullname=fullname)
    await message.answer(text=f'Приятно познакомится, {fullname}. В какую страну вы бы хотели отправиться?')
    await state.set_state(StateOrder.country_state)


@router.message(F.text, StateFilter(StateOrder.country_state))
@error_handler
async def get_country(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_country')
    country_input = message.text
    list_countries: list = await method_get_countries()
    for i, country in list_countries:
        if country == country_input:
            await message.answer(text=f'Прекрасный выбор! Каком городе в стране <b>{country}</b> вы хотели бы остановиться?')
            await state.set_state(StateOrder.city_state)
            await state.update_data(countries=country)
            await state.update_data(country_id=i)
            break
    else:
        await message.answer(text=f'К сожалению в <b>{country_input}</b> мы туры не предоставляем. Укажите другую страну')


@router.message(F.text, StateFilter(StateOrder.city_state))
@error_handler
async def get_city(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_city')
    city_input = message.text
    await state.update_data(city=city_input)
    await message.answer(text=f'Укажите желаемую дату вылета. Формат даты: дд-мм-гггг')
    await state.set_state(StateOrder.data_department_state)


@router.message(F.text, StateFilter(StateOrder.data_department_state))
@error_handler
async def get_data_department(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_data_department')
    data_department_input = message.text
    data_department_ = f'{data_department_input.split("-")[-1]}-{data_department_input.split("-")[1]}-{data_department_input.split("-")[0]}'
    await state.update_data(data_department=data_department_)
    if validate_date_birthday(data_department_input):
        hotel_types_list = ['1*', '2*', '3*', '4*', '5*', '5+*', 'Apts', 'Villa']
        await message.answer(text='Выберите тип отеля',
                             reply_markup=keyboard_hotel_types(hotel_types=hotel_types_list))
    else:
        await message.answer(text=f'Дата введена некорректно. Формат даты: дд-мм-гггг')


@router.callback_query(F.data.startswith('hotel'))
@error_handler
async def get_hotel_types(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info('get_hotel_types')
    hotel_types = callback.data.split('_')[-1]
    await state.update_data(hotel_types=hotel_types)
    nutrition_list = ['RO', 'BB', 'HB', 'HB+', 'FB', 'FB+', 'AI', 'UAI']
    await callback.message.edit_text(text='Выберите тип отеля',
                                     reply_markup=keyboard_nutrition(nutritions=nutrition_list))


@router.callback_query(F.data.startswith('nutrition'))
@error_handler
async def get_hotel_types(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info('get_hotel_types')
    nutrition = callback.data.split('_')[-1]
    await state.update_data(nutrition=nutrition)
    await callback.message.edit_text(text='Укажите желаемое количество ночей')
    await state.set_state(StateOrder.count_night_state)


@router.message(F.text, StateFilter(StateOrder.count_night_state))
@error_handler
async def get_count_night(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_count_night')
    count_night_input = message.text
    await state.update_data(count_night=count_night_input)
    if count_night_input.isdigit() and int(count_night_input) > 0:
        await message.answer(text='Укажите количество туристов')
        await state.set_state(StateOrder.count_tourist_state)
    else:
        await message.answer(text=f'Количество ночей должно быть целым положительным числом')


@router.message(F.text, StateFilter(StateOrder.count_tourist_state))
@error_handler
async def get_count_tourist(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_count_tourist')
    count_tourist_input = message.text
    await state.update_data(count_tourist=count_tourist_input)
    if count_tourist_input.isdigit() and int(count_tourist_input) > 0:
        await message.answer(text='Укажите количество детей')
        await state.set_state(StateOrder.age_kids_state)
    else:
        await message.answer(text=f'Количество туристов указано некорректно,'
                                  f' количество должно быть целым положительным числом')


@router.message(F.text, StateFilter(StateOrder.age_kids_state))
@error_handler
async def get_age_kids(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_age_kids')
    age_kids_input = message.text
    await state.update_data(age_kids=age_kids_input)
    if age_kids_input.isdigit() and int(age_kids_input) >= 0:
        await message.answer(text='Укажите ваш бюджет')
        await state.set_state(StateOrder.budget_state)
    else:
        await message.answer(text=f'Количество детей указано некорректно')


@router.message(F.text, StateFilter(StateOrder.budget_state))
@error_handler
async def get_data_budget(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_data_budget')
    budget_input = message.text
    await state.update_data(budget=budget_input)
    if budget_input.isdigit() and int(budget_input) > 0:
        await request_contact(message=message, state=state, bot=bot)
        await state.set_state(StateOrder.phone_state)
    else:
        await message.answer(text=f'Количество детей указано некорректно')


@router.message(StateFilter(StateOrder.phone_state))
@error_handler
async def get_phone_state(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_phone_state')
    phone_input = await get_phone_user(message=message, state=state, bot=bot)
    if phone_input:
        await message.answer(text='📣',
                             reply_markup=ReplyKeyboardRemove())
        await state.update_data(phone=phone_input)
        list_office = await method_get_company_office()
        await utils_handler_pagination_and_select_item(list_items=list_office,
                                                       text_message_pagination='Выберите офис:',
                                                       page=0,
                                                       count_item_page=6,
                                                       callback_prefix_select='office_select',
                                                       callback_prefix_back='office_back',
                                                       callback_prefix_next='office_next',
                                                       message=message,
                                                       callback=None)


@router.callback_query(F.data.startswith('office'))
async def process_office(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info('process_office')
    page = int(callback.data.split('_')[-1])
    action = callback.data.split('_')[1]
    if action in ['back', 'next']:
        list_office = await method_get_company_office()
        await utils_handler_pagination_and_select_item(list_items=list_office,
                                                       text_message_pagination='Выберите офис:',
                                                       page=page,
                                                       count_item_page=6,
                                                       callback_prefix_select='office_select',
                                                       callback_prefix_back='office_back',
                                                       callback_prefix_next='office_next',
                                                       message=None,
                                                       callback=callback)
    else:
        await callback.message.edit_text(text='Спасибо вам за предоставленные данные, в ближайшее время с вами'
                                              ' свяжется менеджер для уточнее деталей')
        data = await state.get_data()
        id_office = int(callback.data.split('_')[-1])
        format_dict_ = {
            "u_telegram": f'{callback.from_user.username}/{callback.from_user.id}',
            "source": 'tg_bot',
            "u_name": data['fullname'],
            "countries": int(data['country_id']),
            "note": data['city'],
            "data_department": data['data_department'],
            "hotel_types": data['hotel_types'],
            "nutrition": data['nutrition'],
            "nights_to": data['count_night'],
            "tourist_count": data['count_tourist'],
            "tourist_child_count": data['age_kids'],
            "budget": int(data['budget']),
            "u_phone_mobile": data['phone'],
            "r_co_id": id_office
        }
        await method_post_lead(format_dict=format_dict_)
        format_dict_ = {
            "tg_id": callback.from_user.id,
            "fullname": data['fullname'],
            "countries": data['countries'],
            "city": data['city'],
            "data_department": data['data_department'],
            "hotel_types": data['hotel_types'],
            "nutrition": data['nutrition'],
            "nights_to": data['count_night'],
            "tourist_count": data['count_tourist'],
            "tourist_child_count": data['age_kids'],
            "budget": data['budget'],
            "u_phone_mobile": data['phone']
        }
        await rq.add_order(data=format_dict_)