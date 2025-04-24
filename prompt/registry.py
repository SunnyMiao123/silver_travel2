# prompt/registry.py
from prompt.template import PromptTemplate

def get_prompt(agent_type: str) -> PromptTemplate:
    if agent_type == "recommend":
        return PromptTemplate("请根据用户需求推荐国内康养景点。\\n用户：{question}")
    elif agent_type == "itinerary":
        return PromptTemplate( """请根据用户提供的出发地、目的地、出行天数、预算、兴趣，生成一个适合银发族的每日旅游行程安排。
包含每天的景点顺序、餐饮建议、住宿安排、注意事项。\\n用户：{question}""")
    else:
        raise ValueError(f"未知 agent_type: {agent_type}")