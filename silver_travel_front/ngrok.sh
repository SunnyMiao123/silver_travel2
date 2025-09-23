#!/bin/bash

# 启动 ngrok（后台）
echo "🚀 启动 ngrok..."
ngrok http 8000 --log=stdout > .ngrok_raw.log &

# 等待 ngrok 启动（5 秒以内）
sleep 5

# 调用 ngrok 的本地 API 获取公网地址
NGROK_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9\-]*\.ngrok-free\.app' | head -n 1)

if [ -z "$NGROK_URL" ]; then
  echo "❌ 未能获取 ngrok 地址，请确认 ngrok 是否正确启动。"
  exit 1
fi

# 生成对应的 WebSocket 地址（替换 https => wss）
NGROK_WS_URL=$(echo "$NGROK_URL" | sed 's/^https:/wss:/')


# 写入 .env 文件
echo "VITE_API_BASE=$NGROK_URL" > .env.ngrok
echo "VITE_API_WS=$NGROK_WS_URL" >> .env.ngrok
echo "✅ 已生成 .env.ngrok"
cat .env.ngrok
