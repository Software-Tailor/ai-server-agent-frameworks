# AI Server with agent frameworks

The same tool-using agent in each popular Python agent framework, pointed at
**[Software Tailor AI Server](https://softwaretailor.com/docs/ai-server/index.htm)**. That gives you
private, on-premises models behind the framework you already use.

Each example gives the agent one tool (`get_weather`) that returns a unique token. The example passes only if
the final answer contains that token. That proves the whole loop worked: the model made a *structured* tool
call, the framework ran the tool, sent the result back, and the model used it.

| Framework | File | Tested against AI Server |
| --- | --- | --- |
| **LangGraph** (+ LangChain `ChatOpenAI`) | [`python/langgraph_agent.py`](python/langgraph_agent.py) | ✅ pass |
| **LlamaIndex** (`OpenAILike` + `FunctionAgent`) | [`python/llamaindex_agent.py`](python/llamaindex_agent.py) | ✅ pass |
| **Pydantic AI** (`OpenAIChatModel`) | [`python/pydantic_ai_agent.py`](python/pydantic_ai_agent.py) | ✅ pass |
| **OpenAI Agents SDK** (`OpenAIChatCompletionsModel`) | [`python/openai_agents_sdk.py`](python/openai_agents_sdk.py) | ✅ pass |
| **smolagents** (`ToolCallingAgent`) | [`python/smolagents_agent.py`](python/smolagents_agent.py) | ⚠️ 4 of 5 runs (see below) |

Tested with AI Server 2.2.5 and model `enginea/qwen3/8b`, using langchain-openai 1.6, langgraph 1.2,
llama-index-core 0.14, pydantic-ai-slim 2.31, openai-agents 0.20 and smolagents 1.26.

## Run

```bash
cd python
pip install -r requirements.txt            # or just the framework you want
export AISERVER_BASE_URL="http://192.168.1.42:11436/v1"   # from AI Server's Server page — ends in /v1
export AISERVER_API_KEY="ai-suite_..."                     # AI Server -> API keys
export AISERVER_MODEL="enginea/qwen3/8b"                   # a tool-capable model id from GET /v1/models
python run_all.py
```

```
[PASS] LangGraph: The current weather in Dublin is 14°C with light rain and forecast code ZEPHYR-42.
[PASS] LlamaIndex: ...
...
5/5 passed
```

## What each framework needs

| Framework | The setting that matters |
| --- | --- |
| LangGraph / LangChain | `ChatOpenAI(model=..., base_url=..., api_key=...)` — nothing else |
| LlamaIndex | Use `OpenAILike`, not `OpenAI`, and set `is_chat_model=True, is_function_calling_model=True`. LlamaIndex can't infer tool support from an unknown model id. |
| Pydantic AI | `OpenAIChatModel(model, provider=OpenAIProvider(base_url=..., api_key=...))` |
| OpenAI Agents SDK | Use **`OpenAIChatCompletionsModel`**. The default model class speaks the Responses API, which AI Server doesn't implement. Also call **`set_tracing_disabled(True)`**: by default the SDK uploads traces to OpenAI, which a private deployment must not do. |
| smolagents | `OpenAIServerModel(model_id=..., api_base=..., api_key=...)` |

**About smolagents:** it sends `tool_choice: "required"` on every step. AI Server's default local engine does
not yet enforce `"required"`, so the model can occasionally answer in text on a step where smolagents expects
a call. smolagents then retries, and we saw 1 failure in 5 runs. Other frameworks use `"auto"` and are
unaffected. This is tracked by the `tools_required` check in
[ai-server-compat](https://github.com/Software-Tailor/ai-server-compat).

## Choosing a model

Use a general **instruct** model with tool support, 7–8B or larger: Qwen 3 / Qwen 2.5 instruct, Llama 3.1 8B,
or gpt-oss 20B on a GPU. Code-tuned variants (for example "Coder" models) often write tool calls as plain
text instead of structured `tool_calls`. Very small models (≈3B) loop or contradict themselves across steps.

## Related

- [ai-server-security-agents](https://github.com/Software-Tailor/ai-server-security-agents): a SOC triage agent (Python + C#)
- [ai-server-dropin-recipes](https://github.com/Software-Tailor/ai-server-dropin-recipes): Continue, Open WebUI, aider, Semantic Kernel
- [ai-server-compat](https://github.com/Software-Tailor/ai-server-compat): protocol checks and the "Works with AI Server" catalogue
- [Developer hub](https://softwaretailor.com/developers.htm) · [Partner Programme](https://softwaretailor.com/partners/)

MIT licensed. See [LICENSE](LICENSE).
