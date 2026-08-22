import sys

sys.path.append(r"E:\workspace\pro\demo01\study\deep_agents")

from app.core.agents import agent
from app.utils.decorator_utils import timer
from app.utils.log_utils import logger


@timer
def main(user_input: str, history: list = None):
    match user_input:
        case "quit" | "q":
            sys.exit(1)

    logger.info(history)
    history.append({"role": "user", "content": user_input})
    result = agent.invoke(input={"messages": history})
    assistant_reply = result["messages"][-1].content
    print(f"Assistant: {assistant_reply}")
    history.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    history = []
    print("=" * 50, " 开始对话 ", "=" * 50)
    while True:
        user_input = input("You: ")
        main(user_input, history)
