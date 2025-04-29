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
        
        
        

class NextStepDecider:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def decide(self, user_input: str, memory: Dict[str, str]) -> Dict[str, str]:
        """根据用户输入和已有memory决定下一步动作"""
        prompt = f"""你是一个专业的出行推荐智能助手。

用户目标：想获得适合他们需求的景点推荐。

请根据以下内容判断：

1. 如果已有信息已经足够进行推荐（即可以根据地理位置、出行偏好、大致人群判断），请返回：
ACTION: RECOMMEND

2. 如果信息不足，不能准确推荐，请返回：
ACTION: ASK
QUESTION: （用自然、亲切的口吻提出一个补充性问题，引导用户补全信息）

用户输入：
{user_input}

已有信息（Memory）：
{memory}

请严格按照下面格式返回：
ACTION: RECOMMEND
（或者）
ACTION: ASK
QUESTION: xxx
"""

        response = await self.llm.Run(prompt,"",None)

        # 解析 LLM 返回内容
        result = {}
        lines = response.splitlines()
        for line in lines:
            if line.startswith("ACTION:"):
                result["action"] = line.replace("ACTION:", "").strip()
            elif line.startswith("QUESTION:"):
                result["question"] = line.replace("QUESTION:", "").strip()

        return result