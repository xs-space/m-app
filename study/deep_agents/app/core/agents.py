import sys

sys.path.append(r"E:\workspace\pro\demo01\study\deep_agents")

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.chat_models import init_chat_model

from app.conf.settings import settings
from app.utils.log_utils import logger

llm_params = {
    # "model": "qwen3.6:35b",
    "model": settings.model,
    "openai_api_key": settings.api_key,
    "openai_api_base": settings.base_url,
    "model_provider": "openai",
    "temperature": 0,
    "max_retries": 3,
    "streaming": False,
}


logger.info(settings.virtual_path)
logger.info(llm_params)

backend = FilesystemBackend(root_dir=settings.virtual_path, virtual_mode=True)

llm = init_chat_model(**llm_params)

agent = create_deep_agent(
    model=llm,
    system_prompt="你是一个助人为乐的AI",
    backend=backend,
    tools=[],
    debug=False,
)
