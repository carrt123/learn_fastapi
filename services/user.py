from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import User
from db.database import async_engine, Base
from utils.hash_helper import HashHelper


class UserServeries:

    @staticmethod
    async def init_create_table():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_user(async_session: AsyncSession, user_id: int):
        response = select(User).where(User.id == user_id)
        result = await async_session.execute(response)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_name(async_session: AsyncSession, username: str) -> User:
        response = select(User).where(User.username == username)
        result = await async_session.execute(response)
        return result.scalars().first()

    @staticmethod
    async def get_users(async_session: AsyncSession):
        response = select(User).order_by(User.id)
        result = await async_session.execute(response)
        return result.scalars().fetchall()

    @staticmethod
    async def create_user(async_session: AsyncSession, **kwargs):
        new_user = User(**kwargs)
        async_session.add(new_user)
        await async_session.commit()
        return new_user

    @staticmethod
    async def update_user(async_session: AsyncSession, user_id: int, **kwargs):
        response = update(User).where(User.id == user_id)
        result = await async_session.execute(response.values(**kwargs))
        await async_session.commit()
        return result

    @staticmethod
    async def delete_user(async_session: AsyncSession, user_id: int):
        response = delete(User).where(User.id == user_id)
        result = await async_session.execute(response)
        await async_session.commit()
        return result



