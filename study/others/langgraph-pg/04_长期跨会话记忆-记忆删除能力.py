from langchain_openai import ChatOpenAI
from langgraph.store.postgres import PostgresStore

llm = ChatOpenAI(
    model="qwen3.8:27b",
    base_url="http://localhost:11433/v1",
    api_key="dummy",
    temperature=0.7,
    max_tokens=512,
)

if __name__ == "__main__":
    DB_URI = "postgresql://postgres:123456@localhost:5432/ai?sslmode=disable"

    with PostgresStore.from_conn_string(DB_URI) as store:
        store.setup()

        # 定义命名空间
        namespace = ("user_001", "chat")

        # 推送记忆到命名空间
        store.put(namespace, "preference", {"style": "喜欢简短直接回答", "skill": "会Python编程，会使用SQL数据库"})

        store.put(
            namespace,
            "a-memory",
            {
                "rules": [
                    "你是一个专业的Python开发人员",
                    "你只能回答与Python相关的问题",
                    "你只能回答与SQL数据库相关的问题",
                ],
                "my_key": "你好，我想知道Python的版本号",
            },
        )

        # 单独删除一条记忆
        store.delete(namespace, "preference")

        # 循环删除多条
        all_items = store.search(namespace)
        print(f"待删除key列表：{[x.key for x in all_items]}")
        for mem in all_items:
            store.delete(namespace, mem.key)
        print("批量删除完成，剩余记录: ", store.search(namespace))
