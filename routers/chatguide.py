# routers/chatguide.py（真正智能体驱动的重构）

from fastapi import APIRouter,WebSocket
from typing import List, Dict
from httpx import stream
from pydantic import BaseModel
import asyncio
from utils.stream_buffer import StreamBuffer

from routers.factory import AgentFactory
from routers.router import AgentRouter
from agent.session.sessionmanager import SessionManager

# 初始化核心组件
factory = AgentFactory()
agentrouter = AgentRouter(factory)
session_manager = SessionManager()

chat_router = APIRouter(prefix="/chatguide", tags=["chatguide"])

# 请求体定义
class ChatPayload(BaseModel):
    user_id: str
    message: str

@chat_router.post("/message")
async def chat_message(payload: ChatPayload):
    user_id = payload.user_id
    message = payload.message

    # 分发：意图识别 + 智能体调用
    agent = agentrouter.get_agent_by_dispatcher(message,"")
    agent_type = agent.AgentType

    # 注入历史
    history = session_manager.get_history(user_id, agent_type)

    # 调用智能体（要求输出结构化 JSON）
    result = agent.Run(message, chat_history=history)

    # 更新历史
    session_manager.append_turn(user_id, agent_type, "user", message)
    session_manager.append_turn(user_id, agent_type, "assistant", result if isinstance(result, str) else str(result))

    # 统一响应结构：结构化输出 or fallback 文本
    if isinstance(result, dict):
        summary = result.get("summary", "")
        data = result.get("data", {})
        next_step = result.get("next", None)
    else:
        summary = result[:100]
        data = result
        next_step = None

    return {
        "intent": agent_type,
        "agent": agent.__class__.__name__,
        "content": {
            "summary": summary,
            "data": data,
            "next": next_step
        }
    }
from fastapi import WebSocketDisconnect

@chat_router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            userid = data["user_id"]
            message = data["message"]

            # 分发智能体
            agent = agentrouter.get_agent_by_dispatcher(message, userid)
            history = session_manager.get_history(userid, agent.AgentType)

            loop = asyncio.get_running_loop()
            # 建立 Buffer 和 Token 回调
            buffer = StreamBuffer()

            def on_token(token: str):
                buffer.feed(token)
               # asyncio.create_task(websocket.send_text(token))
                loop.create_task(websocket.send_text(token))

            await asyncio.to_thread(
                agent.LLM.callLLM_stream,
                message,
                agent.SystemPrompt,
                on_token,
                history
            )
            # 流式调用
            
            stream_output = buffer.get_full_text()
            # 保存历史 + 最终响应
            session_manager.append_turn(userid, agent.AgentType, "user", message)
            session_manager.append_turn(userid, agent.AgentType, "assistant", stream_output)

            await websocket.send_text("[DONE]")
            await websocket.send_json({
                "intent": agent.AgentType,
                "agent": agent.__class__.__name__,
                "content": {
                    "summary": stream_output[:100],
                    "data": stream_output,
                    "next": None
                }
            })
    except WebSocketDisconnect:
        print("WebSocket closed by client")
    except Exception as e:
        print("WebSocket error:", e)
        await websocket.close()

# ===== 保留原接口不动（结构提取） =====


# 已废弃旧接口 fill_request，统一使用 /message 接口

# 替换原 router 引用
router = chat_router
