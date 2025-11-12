from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config.config_reader import settings
from app.core.logging.logger_main import logger

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
            logger.info("Changes was commited successfully")
        except Exception:
            await session.rollback()
            logger.exception("The session returned an error")
            raise
        finally:
            await session.close()
            logger.info("Session closed successfully")