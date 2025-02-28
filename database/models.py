from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(20), default='none')

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(Integer)
    fullname: Mapped[str] = mapped_column(String(20))
    countries: Mapped[str] = mapped_column(String(20))
    city: Mapped[str] = mapped_column(String())
    data_department: Mapped[str] = mapped_column(String())
    hotel_types: Mapped[str] = mapped_column(String())
    nutrition: Mapped[str] = mapped_column(String())
    nights_to: Mapped[str] = mapped_column(String())
    tourist_count: Mapped[str] = mapped_column(String())
    tourist_child_count: Mapped[str] = mapped_column(String())
    budget: Mapped[int] = mapped_column(Integer())
    u_phone_mobile: Mapped[str] = mapped_column(String())


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

