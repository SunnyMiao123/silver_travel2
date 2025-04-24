from typing import List, Dict, Type
from agent.agentbase import Agent
from agent.RecommendAgent import RecommendAgent
from agent.itinerary import ItineraryAgent
from agent.dispatcher import DispatcherAgent
from agent.commonagent import CommonAgent

class AgentFactory:
    def __init__(self):
        self.registry :Dict[str, Type[Agent]] = {
            "recommend": RecommendAgent,
            "itinerary": ItineraryAgent,
            "dispatcher": DispatcherAgent,
            "other": CommonAgent
        }
        self.default_agent: Type[Agent] = None
        
    def register_agent(self, agent_name: str, agent_class: Type[Agent]) -> None:
        """
        Register an agent class with a name.
        """
        if agent_name in self.registry:
            raise ValueError(f"Agent {agent_name} is already registered.")
        self.registry[agent_name] = agent_class
        
    def get_agent(self,agent_type:str, **kwargs) -> Agent:
        """
        Get an instance of the agent class based on the type.
        """
        if agent_type not in self.registry:
            raise ValueError(f"Agent type {agent_type} is not registered.")
        return self.registry[agent_type](**kwargs)