from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import db_settings


engine = create_async_engine(f"sqlite+aiosqlite:///{db_settings.sqlite_db}")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


async def get_session():
    async with new_session() as session:
        yield session


async def get_db():
    db: AsyncSession = new_session()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
    finally:
        await db.close()
