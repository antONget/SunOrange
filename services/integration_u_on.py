import json
from config_data.config import load_config, Config
import requests
from datetime import datetime
import asyncio
config: Config = load_config()


async def method_get_countries() -> list:
    key = config.u_on.key_uon
    _format = 'json'
    url = f'https://api.u-on.ru/{key}/countries.{_format}'
    response = requests.get(url=url, verify=False)
    return [[country['id'], country['name']] for country in response.json()['records']]


async def method_get_company_office() -> list:
    key = config.u_on.key_uon
    _format = 'json'
    url = f'https://api.u-on.ru/{key}/company-office.{_format}'
    response = requests.get(url=url, verify=False)
    return [[office['id'], office['name']] for office in response.json()['records']]


async def method_post_lead(format_dict: dict) -> None:
    key = config.u_on.key_uon
    _format = 'json'
    url = f'https://api.u-on.ru/{key}/lead/create.{_format}'
    response = requests.post(url=url, data=format_dict, verify=False)
    print(response.text)
#
#
# async def method_add_request(format_dict: dict):
#     format_json = json.dumps(format_dict)
#     key = config.u_on.key_uon
#     _format = 'xml'
#     # url = f'https://api.u-on.ru/{key}/request/create.{_format}'
#     url = f'https://api.u-on.ru/{key}/lead/create.{_format}'
#     response = requests.post(url=url, data=format_dict, verify=False)
#     print(response.status_code)
#     print(response.text)
#
#
# async def method_get_request(format_dict: dict):
#     format_json = json.dumps(format_dict)
#     key = config.u_on.key_uon
#     _format = 'json'
#     # url_get_city = f'https://api.u-on.ru/{key}/cities/{country_id}/{page}.{_format}'
#     # url = f'https://api.u-on.ru/{key}/company-office.{_format}'
#     url = f'https://api.u-on.ru/{key}/countries.{_format}'
#     # url_create_lead = f'https://api.u-on.ru/{key}/lead/create.{_format}'
#     # url = f'https://api.u-on.ru/{key}/nutrition.{_format}'
#     response = requests.get(url=url, verify=False)
#     print(response.status_code)
#     print([[country['id'], country['name']] for country in response.json()['records']])
#
#     # tg_id/username: "u_telegram"
#     # fullname: "u_name"
#     # country*: "countries"
#     # city: "note"
#     # data_department: "date_from"
#     # hotel(1*,2*,3*,4*,5*,5+*,Apts,Villa): "hotel_types"
#     # dish(RO,BB,HB,HB+,FB,FB+,AI,UAI): "nutrition"
#     # count_night: "nights_to"
#     # count_tourist: "tourist_count"
#     # age_kids: "tourist_child_count"
#     # budget: "budget"
#     # phone: "u_phone_mobile"
#     # office*: "r_co_id"
#
# # format_dict_ = {
# #     "r_id_internal": 100,
# #     "source": 'tg_bot',
# #     "note": 'Антон',
# # }
#
# format_dict_ = {
#     "u_telegram": '@AntonPon0marev/843554518',
#     "source": 'tg_bot',
#     "u_name": 'Антон',
#     "countries": 58,
#     "note": 'Мадрид',
#     "data_department": str(datetime.now().strftime('%Y-%m-%d')),
#     "hotel_types": '5+*',
#     "nutrition": 'AI',
#     "nights_to": '10',
#     "tourist_count": '1',
#     "tourist_child_count": '0',
#     "budget": 10000,
#     "u_phone_mobile": '79818074762',
#     "r_co_id": 1
# }


if __name__ == '__main__':
    # asyncio.run(method_add_request(format_dict=format_dict_))
    asyncio.run(method_get_company_office())


# import requests
#
# # URL API
# url = 'https://api.u-on.ru/1ga3bkGsm1km4/lead/create.json'
#
# # Данные, которые собираемся отправить
# data = {
#     'source': 'заявка с сайта',
#     'u_name': input('Введите имя: '),  # Получаем имя от пользователя
#     'u_phone': input('Введите телефон: ')  # Получаем телефон от пользователя
# }
#
# # Выполняем POST-запрос
# response = requests.post(url, data=data, verify=False)
#
# # Печатаем ответ от сервера
# print(response.text)