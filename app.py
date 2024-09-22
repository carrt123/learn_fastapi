from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from dependencies import get_async_session
from sqlalchemy import select
from utils.hash_helper import HashHelper
load_dotenv()
app = FastAPI(title="短链")


@app.on_event("startup")
async def startup_event():
    from db.database import async_engine, Base
    from models.model import User, ShortenUrl

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

    await init_create_table()
    await create_admin_user()


@app.on_event("shutdown")
async def shutdown_event():
    pass


from api.short import router_short
from api.user import router_user

app.include_router(router_short)
app.include_router(router_user)

if __name__ == '__main__':
    uvicorn.run('app:app', host='127.1.1.1', port=5000, reload=True)
