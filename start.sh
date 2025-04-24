#!/bin/bash

# 定义后端 FastAPI 启动命令
start_backend() {
  echo "Starting FastAPI backend..."
  # 启动 FastAPI 服务
  uvicorn main:app --reload --host 127.0.0.1 --port 8090 &
}

# 定义前端 Vite 启动命令
start_frontend() {
  echo "Starting React frontend..."
  # 启动 React + Vite 开发环境
  cd silver_travel_front
  npm run dev
}

# 启动后端
start_backend

# 启动前端
start_frontend