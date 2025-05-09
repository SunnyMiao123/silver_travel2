from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple,Callable

class BaseLLM(ABC):
    """
    Abstract base class for LLMs (Large Language Models).
    """
    def __init__(self, baseURL: str, apikey: str, model: str, temperature: float = 0.7, max_tokens: int = 2048, top_p: float = 1.0, frequency_penalty: float = 0.0):
        self.baseURL = baseURL
        self.apikey = apikey
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty

    @abstractmethod
    def getLLM(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Call the LLM with the given prompt and optional stop sequences.
        """
        return self
    
    @abstractmethod
    def callLLM(self, prompt: str, sys_prompt:str, history: Optional[List[str]] = None) -> str:
        pass
    
    async def async_callLLM(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Asynchronous call to the LLM.
        """
        return self.callLLM(prompt, stop)
    
    @abstractmethod
    def callLLM_stream(
        self, 
        prompt: str, 
        sys_prompt:str, 
        on_token: Callable[[str], None],
        history: Optional[List[str]] = None) -> None:
        """
        Call the LLM with the given prompt and optional stop sequences.
        """
        raise NotImplementedError("This LLM does not support streamLLM()")