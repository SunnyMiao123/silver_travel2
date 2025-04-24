# schemas/user.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    phone: Optional[str] = None
    nickname: Optional[str] = None
    age: Optional[int] = None
    interests: Optional[str] = None

class UserCreate(UserBase):
    phone: str
    password: str

class UserLogin(BaseModel):
    phone: str
    password: str

class UserWeChatLogin(BaseModel):
    code: str  # 微信小程序端通过 wx.login() 获取的 code

class UserOut(UserBase):
    id: int
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True