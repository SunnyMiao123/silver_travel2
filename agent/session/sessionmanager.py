# session/session_manager.py

from typing import Dict, List, Optional
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

