# crud/user.py

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import get_password_hash, verify_password

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def get_user_by_openid(db: Session, openid: str):
    return db.query(User).filter(User.wechat_openid == openid).first()

def create_user_with_phone(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(phone=user.phone, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user_password(db_user: User, password: str):
    return verify_password(password, db_user.password_hash)