"""LlamaIndex FunctionAgent on AI Server.   pip install llama-index-core llama-index-llms-openai-like"""
import asyncio

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai_like import OpenAILike

from common import API_KEY, BASE_URL, MODEL, QUESTION, report, weather


def get_weather(city: str) -> str:
    """Current weather for a city."""
    return weather(city)


# is_chat_model + is_function_calling_model tell LlamaIndex this OpenAI-compatible server supports
# /chat/completions with tools (it cannot infer that from an unknown model id).
llm = OpenAILike(model=MODEL, api_base=BASE_URL, api_key=API_KEY, is_chat_model=True,
                 is_function_calling_model=True, context_window=8192, temperature=0)
agent = FunctionAgent(tools=[FunctionTool.from_defaults(get_weather)], llm=llm,
                      system_prompt="Use tools to answer.")


async def main():
    response = await agent.run(user_msg=QUESTION)
    report("LlamaIndex", str(response))


asyncio.run(main())
