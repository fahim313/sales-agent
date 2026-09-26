from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={
        "server_settings": {
            "search_path": settings.DB_SCHEMA,
        }
    },
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Default for endpoints: commit/rollback runs before the response is sent.
SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]

# Only for endpoints returning a StreamingResponse that reads from the DB
# while streaming. The session stays open until the response is finished.
StreamingSessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]