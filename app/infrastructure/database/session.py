from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config.config_reader import settings

from typing import AsyncGenerator

class Base(AsyncAttrs, DeclarativeBase):
    pass

_engine = create_async_engine(
    url=settings.DATABASE_URL.get_secret_value(),
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

_session_factory = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()