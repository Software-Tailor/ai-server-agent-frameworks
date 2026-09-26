"""OpenAI Agents SDK on AI Server.   pip install openai-agents

Two settings matter for any non-OpenAI server:
  * use OpenAIChatCompletionsModel — the SDK's default model class speaks the Responses API, which AI Server
    does not implement; Chat Completions is fully supported;
  * disable tracing — by default the SDK uploads traces to OpenAI's servers, which is exactly what a
    private deployment is trying to avoid.
"""
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from openai import AsyncOpenAI

from common import API_KEY, BASE_URL, MODEL, QUESTION, report, weather

set_tracing_disabled(True)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY))


@function_tool
def get_weather(city: str) -> str:
    """Current weather for a city."""
    return weather(city)


agent = Agent(name="assistant", instructions="Use tools to answer.", model=model, tools=[get_weather])
report("OpenAI Agents SDK", Runner.run_sync(agent, QUESTION).final_output)
