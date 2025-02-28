from database.models import User, Order
from database.models import async_session
from sqlalchemy import select
from dataclasses import dataclass
import logging
from datetime import datetime

"""USER"""


async def add_user(tg_id: int, data: dict) -> None:
    """
    Добавляем нового пользователя если его еще нет в БД
    :param tg_id:
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # если пользователя нет в базе
        if not user:
            session.add(User(**data))
            await session.commit()


async def add_order(data: dict) -> None:
    """
    Добавляем новую заявку
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        session.add(Order(**data))
        await session.commit()
