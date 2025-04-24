# agent/dispatcher.py

from agent.agentbase import Agent
from prompt.template import PromptTemplate
from llm.doubao import DoubaoLLMDriver
from typing import Dict, List, Optional
# DispatcherAgent 是一个用于分类用户需求的智能体    
# 它使用 Doubao LLM 进行自然语言处理，并根据用户输入的文本进行分类
# 它的主要功能是将用户的需求意图分类为以下四种类型：
# - 景点推荐 → recommend            
# - 行程规划 → itinerary
# - 组团参团 → group
# - 智能相册 → album
# 该智能体的构造函数初始化了一个提示模板，并设置了系统提示
# 该提示模板用于指导 LLM 如何处理用户输入
# 该智能体的 run 方法接受用户输入文本，并返回分类结果
# 该方法首先格式化提示模板，然后调用 LLM 进行推理
# 最后，它返回分类结果
# 该智能体的 run 方法还接受一个可选的聊天历史参数
# 该参数用于存储与用户的对话历史
# 如果没有提供聊天历史，它将使用一个空列表
# 该智能体的 run 方法返回的分类结果是一个字符串

class DispatcherAgent(Agent):
    def __init__(self):
        template = """请从以下选项中选择用户的需求意图：
- 景点推荐 → recommend
- 行程规划 → itinerary
- 组团参团 → group
- 智能相册 → album
- 以上均不是 → other

只返回一个单词作为分类结果，不要解释。

用户输入：{question}
分类："""

        super().__init__(
            agent_type="dispatcher",
            llm=DoubaoLLMDriver(),
            prompt_template=PromptTemplate(template),
            system_prompt="你是一个任务分类助手，请根据用户输入判断需求类型。"
        )

    def Run(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
       # prompt = self.PromptTemplate.format(question=input_text)
        result = self.LLM.callLLM(prompt=self.PromptTemplate.format(question=input_text),sys_prompt=self.SystemPrompt, history= chat_history or [])
        return result.strip().lower()
    
    def Run_Stream(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None, on_token=None):
        prompt = self.PromptTemplate.format(question=input_text)
        self.LLM.callLLM(prompt, self.SystemPrompt, chat_history or [], on_token=on_token)
        # 该方法暂时不支持流式输出
