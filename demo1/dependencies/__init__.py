from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from demo1.db.database import AsyncSessionLocal
from contextlib import asynccontextmanager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_session = None
    try:
        db_session = AsyncSessionLocal()
        yield db_session
    finally:
        await db_session.close()


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
