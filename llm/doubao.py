# llm/doubao.py
import requests
from llm.llm import BaseLLM
from typing import List, Dict, Callable
import os
from config import DOUBAO_API_KEY
from volcenginesdkarkruntime import Ark


class DoubaoLLMDriver(BaseLLM):
    def __init__(self):
        super().__init__(
            baseURL="https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            apikey=DOUBAO_API_KEY,
            model="doubao-1-5-pro-32k-250115"
        )
        

    def callLLM(self, prompt: str, sys_prompt: str, history: List[Dict]) -> str:
        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})
        messages.extend(history or [])
        messages.append({"role": "user", "content": prompt})

        client = Ark(api_key=self.apikey)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            stream=False
        )
        #response.raise_for_status()
        return response.choices[0].message.content
    
    def getLLM(self, prompt, stop = None):
        return super().getLLM(prompt, stop)
    
    def callLLM_stream(
        self, 
        prompt: str, 
        sys_prompt:str, 
        on_token: Callable[[str], None],
        history: List[Dict] = None
    ) -> None:
        """
        Call the LLM with the given prompt and optional stop sequences.
        """
        client = Ark(api_key=self.apikey)
        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})
        messages.extend(history or [])
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices:
                message = chunk.choices[0].delta.content
                if message:
                    on_token(message)
        return response
