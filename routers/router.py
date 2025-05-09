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
        self.default_memory: Optional[MemoryDriver] = None
        self.session_cache: Dict[str, Dict[str, Any]] = {}
    
    def get_agent_by_dispatcher(self, message: str, session_id: Optional[str]) -> Agent:
        """
        Get the agent name for a specific intent using the dispatcher.
        """
        if not self.dispatcher:
            raise ValueError("Dispatcher agent is not set.")
        intend = self.dispatcher.Run(message)
        return self.factory.get_agent(intend)