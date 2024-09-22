from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))
    # hashed_password = Column(String(50))
    create_at = Column(DateTime(), default=datetime.now)


class ShortenUrl(Base):
    __tablename__ = "short_url"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_tag = Column(String(20), nullable=False)
    short_url = Column(String(20))
    long_url = Column(String, nullable=False)
    visits_count = Column(Integer, default=0)
    created_at = Column(DateTime(), default=datetime.now)

    create_by = Column(Integer, ForeignKey("users.id"))
    mes_content = Column(String, nullable=False)