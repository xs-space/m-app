import os

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model


def get_weather(city: str) -> str:
    """获取天气的工具"""
    return f"{city} 天气多云转小雨"


llm = init_chat_model(
    model="qwen3.8:27b",
    openai_api_key=os.getenv("API_KEY"),
    openai_api_base=os.getenv("BASE_URL"),
    model_provider="openai",
    temperature=0,
    max_retries=3,
    streaming=False,
)

agent = create_deep_agent(
    model=llm,
    system_prompt="你是一个助人为乐的AI",
    tools=[get_weather],
    debug=True,
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
