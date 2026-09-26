"""LangGraph ReAct agent on AI Server.   pip install langchain-openai langgraph"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from common import API_KEY, BASE_URL, MODEL, QUESTION, report, weather


@tool
def get_weather(city: str) -> str:
    """Current weather for a city."""
    return weather(city)


llm = ChatOpenAI(model=MODEL, base_url=BASE_URL, api_key=API_KEY, temperature=0)
agent = create_react_agent(llm, [get_weather])
result = agent.invoke({"messages": [("user", QUESTION)]})
report("LangGraph", result["messages"][-1].content)
