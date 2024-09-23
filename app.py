from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from dependencies import get_async_session
from sqlalchemy import select
from utils.hash_helper import HashHelper
from db.database import async_engine, Base
from models.model import User, ShortenUrl
from api.short import router_short
from api.user import router_user

load_dotenv()


async def init_create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_admin_user():
    async with get_async_session() as session:  # 使用 context manager
        async with session.begin():
            # 检查是否已经有admin用户
            result = await session.execute(select(User).filter_by(username="admin"))
            admin_user = result.scalar_one_or_none()

            if not admin_user:
                # 创建 admin 用户
                hash_password = HashHelper().hash_password("admin")
                admin_user = User(username="admin", password=hash_password)  # 密码加密逻辑可以在此加入
                session.add(admin_user)
                await session.commit()


async def lifespan(app: FastAPI):
    # 应用启动时执行
    await init_create_table()
    await create_admin_user()

    yield  # 应用运行时的生命周期

    # 应用关闭时执行
    # 如果有需要执行的清理逻辑，可以放在这里
    pass

# 创建 FastAPI 应用，传入 lifespan 事件处理函数
app = FastAPI(title="短链", lifespan=lifespan)

# 添加路由
app.include_router(router_short)
app.include_router(router_user)

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080, reload=True)
