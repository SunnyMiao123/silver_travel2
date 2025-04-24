# agent/base.py
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type
from llm.llm import BaseLLM
from memory.base import MemoryDriver
from prompt.template import PromptTemplate
from tool.base import Tool

class Agent(ABC):
    def __init__(
        self,
        agent_type: str,
        llm: BaseLLM,
        prompt_template: PromptTemplate,
        tools: Optional[List[Tool]] = None,
        memory: Optional[MemoryDriver] = None,
        input_schema: Optional[Type] = None,
        output_schema: Optional[Type] = None,
        system_prompt: Optional[str] = None,
        user_context: Optional[Dict] = None,
        logger: Optional[Any] = None,
        callbacks: Optional[List[Callable]] = None,
        output_serializer: Optional[Callable] = None,
        llm_config: Optional[Dict] = None,
    ):
        self.AgentType = agent_type
        self.LLM = llm
        self.PromptTemplate = prompt_template
        self.Tools = tools or []
        self.ChatHistory = []
        self.Memory = memory
        self.InputSchema = input_schema
        self.OutputSchema = output_schema
        self.SystemPrompt = system_prompt
        self.UserContext = user_context or {}
        self.Logger = logger
        self.Callbacks = callbacks or []
        self.OutputSerialization = output_serializer
        self.LLMConfig = llm_config or {}
        self.Output = None

    @abstractmethod
    def Run(self, input_data: Any) -> Any: ...
    
    @abstractmethod
    def Run_Stream(self, input_text: str, chat_history: Optional[List[Dict[str, str]]] = None, on_token: Optional[Callable] = None) -> None: 
        """如果 Agent 支持流式输出，可重载这个方法"""
        raise NotImplementedError("This agent does not support streaming.")

    def CallLLM(self, input_text: str) -> str:
        prompt = self.PromptTemplate.format(question=input_text)
        return self.LLM.callLLM(prompt=prompt, sys_prompt=self.SystemPrompt, history=self.ChatHistory)

    async def AsyncCall(self, input_text: str) -> str:
        prompt = self.PromptTemplate.format(question=input_text)
        return await self.LLM.asyncCallLLM(prompt=prompt, sys_prompt=self.SystemPrompt, history=self.ChatHistory)

    def InjectMemory(self, data: Dict[str, Any]) -> None:
        if self.Memory:
            self.Memory.save(data)
