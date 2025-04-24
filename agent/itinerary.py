# agent/itinerary.py

from agent.agentbase import Agent
from llm.doubao import DoubaoLLMDriver
from prompt.registry import get_prompt
from prompt.template import PromptTemplate
from typing import List, Dict, Optional

class ItineraryAgent(Agent):
    def __init__(self):
        prompt_template: PromptTemplate = get_prompt("itinerary")
        system_prompt = "你是一位专为老年人定制旅游行程的规划师，擅长合理安排每日活动、饮食与住宿。"

        super().__init__(
            agent_type="itinerary",
            llm=DoubaoLLMDriver(),
            prompt_template=prompt_template,
            system_prompt=system_prompt,
        )

    def Run(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        prompt = self.PromptTemplate.format(question=input_text)
        result = self.LLM.callLLM(prompt=prompt, sys_prompt=self.SystemPrompt, history=chat_history or [])
        return result.strip()
    def Run_Stream(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None, on_token=None):
        prompt = self.PromptTemplate.format(question=input_text)
        self.LLM.callLLM_stream(prompt, self.SystemPrompt, chat_history or [], on_token=on_token)
