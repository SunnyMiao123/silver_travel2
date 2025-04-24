# routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserCreate, UserLogin, UserOut, UserWeChatLogin
from crud import user as crud_user
from utils.security import create_access_token
from models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from typing import Optional
import requests

router = APIRouter(prefix="/users", tags=["users"])

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# 当前登录用户获取
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效 token")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效 token")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

# 用户注册
@router.post("/register", response_model=UserOut)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_phone(db, user_create.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="手机号已注册")
    user = crud_user.create_user_with_phone(db, user_create)
    return user

# 用户登录
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_phone(db, login_data.phone)
    if not db_user or not crud_user.verify_user_password(db_user, login_data.password):
        raise HTTPException(status_code=400, detail="手机号或密码错误")
    access_token = create_access_token(data={"sub": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户信息
@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

# 微信登录（通过 code 获取 openid）
@router.post("/wx_login")
def wx_login(data: UserWeChatLogin, db: Session = Depends(get_db)):
    from config import WECHAT_APPID, WECHAT_SECRET
    wx_api = f"https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": WECHAT_APPID,
        "secret": WECHAT_SECRET,
        "js_code": data.code,
        "grant_type": "authorization_code"
    }
    res = requests.get(wx_api, params=params).json()
    openid = res.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="微信登录失败")

    # 查找或创建用户
    user = crud_user.get_user_by_openid(db, openid)
    if not user:
        user = User(wechat_openid=openid)
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}