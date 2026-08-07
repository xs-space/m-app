import os

from dotenv import load_dotenv

load_dotenv()

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_community.tools import WriteFileTool, ReadFileTool, ListDirectoryTool

list_dir = ListDirectoryTool()


os.environ["OPENAI_API_KEY"] = os.getenv("LOCAL_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("LOCAL_BASE_URL")
model = f"openai:{os.getenv('LOCAL_MODEL')}"

agent = create_deep_agent(
    model=model,
    tools=[list_dir],
    system_prompt="你是一个助手，会用工具计算、读写文件、列出目录。",
    skills=[".skills"],
    backend=FilesystemBackend(root_dir=os.getcwd()),
    debug=True
)

result = agent.invoke({"messages": [{"role": "user", "content": "列出当前目录文件"}]})
print(result['messages'][-1].content)