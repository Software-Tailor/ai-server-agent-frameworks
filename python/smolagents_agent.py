"""Hugging Face smolagents ToolCallingAgent on AI Server.   pip install smolagents"""
from smolagents import OpenAIServerModel, ToolCallingAgent, tool

from common import API_KEY, BASE_URL, MODEL, QUESTION, report, weather


@tool
def get_weather(city: str) -> str:
    """Current weather for a city.

    Args:
        city: The city name.
    """
    return weather(city)


model = OpenAIServerModel(model_id=MODEL, api_base=BASE_URL, api_key=API_KEY)
agent = ToolCallingAgent(tools=[get_weather], model=model, max_steps=6, verbosity_level=0)
report("smolagents", str(agent.run(QUESTION)))
