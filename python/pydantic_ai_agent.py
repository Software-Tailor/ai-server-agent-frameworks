"""Pydantic AI agent on AI Server.   pip install "pydantic-ai-slim[openai]" """
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from common import API_KEY, BASE_URL, MODEL, QUESTION, report, weather

model = OpenAIChatModel(MODEL, provider=OpenAIProvider(base_url=BASE_URL, api_key=API_KEY))
agent = Agent(model, system_prompt="Use tools to answer.")


@agent.tool_plain
def get_weather(city: str) -> str:
    """Current weather for a city."""
    return weather(city)


report("Pydantic AI", agent.run_sync(QUESTION).output)
