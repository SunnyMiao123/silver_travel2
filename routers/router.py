from typing import List, Dict, Any,Dict, Optional, Tuple,Callable
from routers.factory import AgentFactory
from memory.base import MemoryDriver
from llm.llm import BaseLLM
from agent.agentbase import Agent

class AgentRouter:
    def __init__(self, agent_factory: AgentFactory):
        self.factory = agent_factory
        self.dispatcher = self.factory.get_agent("dispatcher")
        self.route_map: Dict[str, str] = {}
        self.intent_classifier: Optional[Callable[[str], str]] = None
        self.default_agent: Optional[str] = None
        self.default_memory: Optional[MemoryDriver] = None
        self.default_llm: Optional[BaseLLM] = None
        self.session_cache: Dict[str, Dict[str, Any]] = {}
        
    def add_route(self, intent: str, agent_name: str) -> None:
        """
        Add a route for a specific intent to an agent.
        """
        if intent in self.route_map:
            raise ValueError(f"Intent {intent} is already mapped to an agent.")
        self.route_map[intent] = agent_name
        
    def route_by_keyword(self, text: str) -> str:
        """
        Simple keyword-based intent classifier.
        """
        for k,v in self.route_map.items():
            if k in text:
                return v
        return None
    def get_agent(self, intent: str,session_id:Optional[str]) -> Optional[str]:
        """
        Get the agent name for a specific intent.
        """
        agent_type = self.route_by_keyword(intent)
        if not agent_type and self.intent_classifier:
            agent_type = self.intent_classifier(intent)
        if not agent_type:
            agent_type = "default"
        if session_id:
            self.session_cache[session_id] = agent_type
        return self.factory.get_agent(agent_type)
    
    def get_agent_by_dispatcher(self, message: str, session_id: Optional[str]) -> Agent:
        """
        Get the agent name for a specific intent using the dispatcher.
        """
        if not self.dispatcher:
            raise ValueError("Dispatcher agent is not set.")
        intend = self.dispatcher.Run(message)
        return self.factory.get_agent(intend)