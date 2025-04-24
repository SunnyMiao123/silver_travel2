# models/user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    password_hash = Column(String, nullable=True)  # 密码加密后保存

    wechat_openid = Column(String(64), unique=True, nullable=True)
    nickname = Column(String(50), nullable=True)
    avatar_url = Column(String(255), nullable=True)

    age = Column(Integer, nullable=True)
    interests = Column(String, nullable=True)  # 可用英文逗号分隔的标签，如 "自然风光,人文历史"

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())