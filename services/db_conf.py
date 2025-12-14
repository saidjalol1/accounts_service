from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pytz

from decouple import config

DATABASE_URL = config("DATABASE_URL")


engine = create_async_engine(
    DATABASE_URL,
    echo=True,  )


async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


def current_time():
    tz = pytz.timezone('Asia/Tashkent')
    return datetime.now(tz)