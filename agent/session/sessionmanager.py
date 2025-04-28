# session/session_manager.py

from typing import Dict, List, Optional
from urllib import response

from agent.agentbase import Agent
from llm.llm import BaseLLM
# SessionManager 是一个用于管理用户会话的类
# 它负责存储和处理用户与智能体之间的对话历史
# 该类提供了多种方法来获取、添加和清除会话数据
# 该类的主要功能包括：
# - 获取用户在某个智能体类型下的历史记录
# - 添加一轮对话（可用于 user/assistant）
# - 清除某个智能体下的会话历史
# - 清除该用户所有的会话数据
# - 获取用户在某个智能体类型下的会话摘要
# - 获取用户在某个智能体类型下的会话摘要（格式化）
# - 获取用户在某个智能体类型下的会话摘要（裸输出）
# - 获取用户在某个智能体类型下的会话摘要（格式化，默认裸输出）
# - 获取用户在某个智能体类型下的会话摘要（格式化，默认裸输出，带参数）

class SessionManager:
    def __init__(self):
        # 会话结构: session_data[user_id][agent_type] = List[Dict[str, str]]
        self.session_data: Dict[str, Dict[str, List[Dict[str, str]]]] = {}

    def get_history(self, user_id: str, agent_type: str) -> List[Dict[str, str]]:
        """获取当前用户在某个智能体类型下的历史记录"""
        return self.session_data.get(user_id, {}).get(agent_type, [])
    
    def get_history_all(self, user_id: str) -> List[Dict[str, str]]:
        if user_id not in self.session_data:
            return []
        merged_history = []
        agent_histories = self.session_data[user_id]
        for agent_type, history in agent_histories.items():
            for h in history:
                merged_item = {
                    "role": h["role"],
                    "content": h["content"],
                    "agent_type": agent_type  # 加上agent类型标记，方便后面追溯
                }
                merged_history.append(merged_item)

        # （可选）按时间排序，如果你记录了时间戳的话
        # merged_history.sort(key=lambda x: x.get("timestamp", 0))

        return merged_history
    
    async def get_user_summary(cls, user_id: str,llm:BaseLLM) -> str:
        """获取用户在某个智能体类型下的会话摘要"""
        history = cls.get_history_all(user_id)
        if not history:
            return "没有历史记录"
        
        # 这里可以调用 LLM 来生成摘要
        summarizer = HistorySummarizer(llm)
        summary = await summarizer.summarize_history(history)
        return summary
    
       

    def append_turn(self, user_id: str, agent_type: str, role: str, content: str):
        """添加一轮对话（可用于 user/assistant）"""
        if user_id not in self.session_data:
            self.session_data[user_id] = {}
        if agent_type not in self.session_data[user_id]:
            self.session_data[user_id][agent_type] = []
        self.session_data[user_id][agent_type].append({
            "role": role,
            "content": content
        })

    def clear_history(self, user_id: str, agent_type: str):
        """清除某个智能体下的会话历史"""
        if user_id in self.session_data and agent_type in self.session_data[user_id]:
            self.session_data[user_id][agent_type] = []

    def reset_user(self, user_id: str):
        """清除该用户所有的会话数据"""
        if user_id in self.session_data:
            del self.session_data[user_id]
            
    def get_summary(self, user_id: str, agent_type: str, format_template: Optional[str] = None) -> str:
        history = self.get_history(user_id, agent_type)
        formatted_history = "\n".join(f"{h['role']}：{h['content']}" for h in history[-6:])
    
        if format_template:
            return format_template.format(history=formatted_history)
        # 默认裸输出
        return formatted_history
    
class HistorySummarizer:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def summarize_history(self, history: List[Dict[str, str]]) -> str:
        history_text = "\n".join(f"{h['role']}：{h['content']}" for h in history[-6:1])
        prompt = f"""
        请根据以下对话记录生成摘要,总结出用户的主要意图和需求，用一句简洁的话概括。不要出现对话内容本身，不要逐句复述。
        聊天记录：
        {history_text}"""
        response = self.llm.callLLM(prompt,"",history)
        return response.strip()
    
    