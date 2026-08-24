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
    assistant_reply = ""
    print("Assistant:")
    for chunk in agent.stream(input={"messages": history}, stream_mode="messages", version="v2"):
        content = chunk["data"][0].content
        assistant_reply = assistant_reply + content
        print(content, end="")
    print("\n")
    history.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    history = []
    print("=" * 50, " 开始对话 ", "=" * 50)
    while True:
        user_input = input("You: ")
        main(user_input, history)
