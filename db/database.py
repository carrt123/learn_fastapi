from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
# URL地址格式
from config.config import get_settings
# 创建异步引擎对象
async_engine = create_async_engine(get_settings().ASYNC_DATABASE_URI, echo=False, future=True)
# 创建ORM模型基类
Base = declarative_base()
# 创建异步的会话管理对象
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)
