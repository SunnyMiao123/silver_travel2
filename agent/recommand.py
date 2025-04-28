# agent/recommend.py

from agent.agentbase import Agent
from llm.doubao import DoubaoLLMDriver
from prompt.registry import get_prompt
from typing import Optional, List, Dict
from prompt.template import PromptTemplate

class RecommendAgent(Agent):
    def __init__(self):
        prompt_template: PromptTemplate = get_prompt("recommend")
        system_prompt = "你是一位经验丰富的老年旅游顾问，擅长推荐适合康养、休闲的国内景点。"

        super().__init__(
            agent_type="recommend",
            llm=DoubaoLLMDriver(),
            prompt_template=prompt_template,
            system_prompt=system_prompt
        )

    def Run(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        prompt = self.PromptTemplate.format(question=input_text)
        result = self.LLM.callLLM(prompt=prompt, sys_prompt=self.SystemPrompt, history=chat_history or [])
        return result.strip()

    def Run_Stream(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None, on_token=None):
        prompt = self.PromptTemplate.format(question=input_text)
        self.LLM.callLLM_stream(prompt, self.SystemPrompt, chat_history or [], on_token=on_token)