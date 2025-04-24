from agent.agentbase import Agent
from typing import Any, Dict, List, Optional, Type
from llm.doubao import DoubaoLLMDriver
from prompt.template import PromptTemplate

class CommonAgent(Agent):
    def __init__(self):
        prompt_template = PromptTemplate("你是一个陪伴式对话助手，语气温和，鼓励用户多表达自己。\n用户：{question}")
        super().__init__(
            agent_type="other",
            llm=DoubaoLLMDriver(),
            prompt_template=prompt_template,
            system_prompt="你是一个温柔的陪聊机器人，擅长关心用户情绪和聊天。"
        )

    def Run(self, input_text: str, chat_history=None):
        prompt = self.PromptTemplate.format(question=input_text)
        result = self.LLM.callLLM(prompt, self.system_prompt, chat_history or [])
        return {
            "summary": "日常聊天回复",
            "data": result,
            "next": None
        }
    def Run_Stream(self, input_text: str, chat_history=None, on_token=None):
        prompt = self.PromptTemplate.format(question=input_text)
        self.LLM.callLLM_stream(prompt, self.system_prompt, chat_history or [], on_token=on_token)
