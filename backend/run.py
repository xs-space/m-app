from pathlib import Path

from icecream import ic

from app.agent.agent import Agent
from app.llm import DeepSeek
from app.memory import Memory
from app.tool.weather_tool import WeatherTool
from app.tool.file_tool import FileTool
from app.tool.todo_tool import TodoTool

if __name__ == "__main__":
    print(Path.cwd())
    agent = Agent(
        session_id="axxxx",
        name="test",
        system_prompt="你是一个本地用户助手，可以帮助用户处理本地工作。",
        llm=DeepSeek(model="qwen3.8:27b"),
        tools=[WeatherTool(), FileTool(work_dir=Path.cwd() / "work_dir"), TodoTool()],
        memory=Memory(),
    )
    res = agent.run("查看下当前文件夹")
    ic(res)
