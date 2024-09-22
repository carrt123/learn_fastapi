from pydantic.v1 import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # 定义连接异步引擎数据库的URL地址
    ASYNC_DATABASE_URI: str = "sqlite+aiosqlite:///shortlink.db"
    # 定义TOKEN的签名信息值
    TOKEN_SIGN_SECRET: str = os.getenv("TOKEN_SIGN_SECRET")


@lru_cache()
def get_settings():
    return Settings()
