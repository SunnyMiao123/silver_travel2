
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user as user_router
from routers import chatguide
from database import Base, engine

app = FastAPI(title="银发旅游小程序后端")

# 创建数据库表
Base.metadata.create_all(bind=engine)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React 开发地址（也可用 ["*"] 临时通配）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册路由
app.include_router(user_router.router)
app.include_router(chatguide.router)