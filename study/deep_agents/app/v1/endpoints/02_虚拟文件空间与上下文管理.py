import sys

sys.path.append(r"E:\workspace\pro\demo01\study\deep_agents")

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.chat_models import init_chat_model

from app.conf.settings import settings
from app.utils.log_utils import logger

logger.info(settings.virtual_path)
logger.info(settings.model)
logger.info(settings.api_key)
logger.info(settings.base_url)
backend = FilesystemBackend(
    root_dir=settings.virtual_path,
    virtual_mode=True,
)

llm = init_chat_model(
    # model=settings.model,
    model="qwen3.6:35b",
    openai_api_key=settings.api_key,
    openai_api_base=settings.base_url,
    model_provider="openai",
    temperature=0,
    max_retries=3,
    request_timeout=600,
    streaming=False,
)

agent = create_deep_agent(
    model=llm,
    system_prompt="你是一个助人为乐的AI",
    backend=backend,
    tools=[],
    debug=False,
)

if __name__ == "__main__":
    history = []
    print("=" * 50, " 开始对话 ", "=" * 50)
    while True:
        user_input = input("You: ")
        match user_input:
            case "quit":
                break
            case "q":
                break

        history.append({"role": "user", "content": user_input})
        result = agent.invoke(input={"messages": history})
        assistant_reply = result["messages"][-1].content
        print(f"Assistant: {assistant_reply}")
        history.append({"role": "assistant", "content": assistant_reply})
