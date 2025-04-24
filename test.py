
"""
from llm.doubao import DoubaoLLMDriver

doubao_llm = DoubaoLLMDriver()
res = doubao_llm.callLLM("介绍一个适合老年人旅游的路线", "你是一个适合老年人的出行助手。", [])
print(res)
"""


"""
from agent.dispatcher import DispatcherAgent

dispatcher = DispatcherAgent()
result = dispatcher.Run("介绍一个适合老年人旅游的路线",[])
print(result)
"""
"""
from agent.RecommendAgent import RecommendAgent
recommend_agent = RecommendAgent()
result = recommend_agent.Run("推荐一个适合老年人的景区", [])
print(result)
"""
"""
from agent.itinerary import ItineraryAgent
itinerary_agent = ItineraryAgent()
result = itinerary_agent.Run("推荐一个适合老年人的旅游路线", [])
print(result)

"""


import os 
print(os.getenv("DOUBAO_APIKEY"))