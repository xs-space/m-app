from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver

llm = ChatOpenAI(
    model="qwen3.8:27b",
    base_url="http://localhost:11434/v1",
    api_key="sk-1234",
    temperature=0.7,
    max_tokens=512,
)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def create_agent(model, tools, checkpointer):
    """构建简单对话 带checkpoint持久化记忆"""

    def chatbot_node(state: AgentState):
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("chatbot", chatbot_node)
    builder.add_edge(START, "chatbot")

    graph = builder.compile(checkpointer=checkpointer)
    return graph


def chat_demo(agent, thread_id: str, user_input: str):
    """单次对话 返回大模型输出"""
    config = {"configurable": {"thread_id": thread_id}}
    resp = agent.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
    return resp["messages"][-1].content


if __name__ == "__main__":
    DB_URI = "postgresql://postgres:123456@localhost:5432/ai?sslmode=disable"

    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        checkpointer.setup()
        agent = create_agent(llm, [], checkpointer=checkpointer)

        print("[会话A：thread_id=user_001]")
        res1 = chat_demo(agent, thread_id="user_001", user_input="你好，我叫王瑞，今年28岁")
        print(f"AI：{res1}\n")

        res2 = chat_demo(agent, thread_id="user_001", user_input="我叫什么名字？多大？")
        print(f"AI：{res2}\n")

        print("[会话B：thread_id=user_002 全新会话，看不到user_001信息]")
        res3 = chat_demo(agent, thread_id="user_002", user_input="我叫什么名字？多大？")
        print(f"AI：{res3}\n")

        print("[模拟程序重启效果：重新获取agent，同一个thread_id依然能记住]")
        agent_new = create_agent(llm, [], checkpointer=checkpointer)
        res4 = chat_demo(agent_new, thread_id="user_001", user_input="再复述一遍我的个人信息")
        print(f"AI：{res4}\n")
