from typing_extensions import TypedDict
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.postgres import PostgresStore

llm = ChatOpenAI(
    model="qwen3.8:27b",
    base_url="http://localhost:11433/v1",
    api_key="dummy",
    temperature=0.7,
    max_tokens=512,
)


@dataclass
class Context:
    """传给智能体的上下文，携带用户编号"""

    user_id: str


class UserInfo(TypedDict):
    """用户信息数据结构"""

    name: str
    hobby: str


# ---------------------- 工具：读取用户长期记忆 ----------------------
@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """查询用户档案信息，当需要获取用户姓名、爱好时调用该工具"""
    store = runtime.store
    user_id = runtime.context.user_id
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "未知用户，档案不存在"


# ---------------------- 工具：保存用户长期记忆 ----------------------
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """保存用户档案，用户告知自己姓名、爱好时调用，参数传入用户信息字典"""
    store = runtime.store
    user_id = runtime.context.user_id
    store.put(("users",), user_id, user_info)
    return "用户信息保存成功"


# ---------------------- 工具：删除用户长期记忆 ----------------------
@tool
def delete_user_memory(runtime: ToolRuntime[Context]) -> str:
    """清除该用户全部档案记忆，用户要求删除个人信息时调用"""
    store = runtime.store
    user_id = runtime.context.user_id
    store.delete(namespace=("users",), key=user_id)
    return f"已清除用户 {user_id} 的档案记忆"


if __name__ == "__main__":
    DB_URI = "postgresql://langgraph_user:1233@localhost:5432/langgraph_db?sslmode=disable"

    with PostgresStore.from_conn_string(DB_URI) as store:
        store.setup()
        test_users = [
            {"user_id": "user_123", "info": {"name": "张三", "hobby": "爬山阅读"}},
            {"user_id": "user_789", "info": {"name": "王五", "hobby": "摄影，骑行"}},
            {"user_id": "user_999", "info": {"name": "赵六", "hobby": "编程，打游戏"}},
        ]

        for item in test_users:
            store.put(("users",), item["user_id"], item["info"])

        agent = create_agent(
            model=llm, tools=[get_user_info, save_user_info, delete_user_memory], store=store, context_schema=Context
        )

        # Agent工具查询用户档案信息
        print("-----------------查询用户档案信息 -----------------")
        resp_read = agent.invoke(
            {"messages": [HumanMessage(content="帮我查一下我的个人档案")]}, context=Context(user_id="user_123")
        )
        print(f"智能体回答：{resp_read['messages'][-1].content}")

        # Agent工具保存用户档案
        print("-----------------保存用户档案 -----------------")
        resp_write = agent.invoke(
            {"messages": [HumanMessage(content="我叫李四，平时爱好打篮球")]}, context=Context(user_id="user_456")
        )
        print(f"智能体回答：{resp_write['messages'][-1].content}")

        saved = store.get(("users",), "user_456")
        print(f"数据库校验保存结果: {saved.value if saved else None}")

        # Agent工具删除用户档案
        print("-----------------删除用户档案 -----------------")
        resp_del = agent.invoke(
            {"messages": [HumanMessage(content="请删除我的个人档案信息")]}, context=Context(user_id="user_456")
        )
        print(f"智能体回答：{resp_del['messages'][-1].content}")

        check_del = store.get(("users",), "user_456")
        print(f"删除后校验档案：{check_del}")
