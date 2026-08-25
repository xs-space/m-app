import sys

sys.path.append(r"E:\workspace\pro\demo01\study\deep_agents")

from typing import Any
from collections.abc import Callable

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.skills import SkillsMiddleware
from langchain.agents.middleware import before_model, after_model, wrap_tool_call, AgentState
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import Command

from app.conf.settings import settings
from app.utils.log_utils import logger


@wrap_tool_call
def log_tool_calls(
    request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    print(f"\n调用工具：{request.tool_call['name']}")
    result = handler(request)
    print(f"\n工具调用完成：{request.tool_call['name']}")
    return result


@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 100:
        return {"messages": [AIMessage("对话已达上限")], "jump_to": "end"}
    return None


@after_model(can_jump_to=["end"])
def log_response(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"\n模型调用结束")
    return None


llm_params = {
    # "model": "qwen3.6:35b",
    "model": settings.model,
    "openai_api_key": settings.api_key,
    "openai_api_base": settings.base_url,
    "model_provider": "openai",
    "temperature": 0,
    "max_retries": 3,
    "streaming": True,
}


logger.info(settings.virtual_path)
logger.info(llm_params)

# backend = FilesystemBackend(root_dir=settings.virtual_path, virtual_mode=True)
skill_backend = FilesystemBackend(root_dir=r"E:\workspace\pro\demo01\study\deep_agents", virtual_mode=True)

llm = init_chat_model(**llm_params)

skill_middleware = SkillsMiddleware(backend=skill_backend, sources=["/skills"])

agent = create_deep_agent(
    model=llm,
    system_prompt="你是一个助人为乐的中文AI",
    backend=skill_backend,
    tools=[],
    middleware=[skill_middleware, log_tool_calls, check_message_limit, log_response],
    debug=False,
)
