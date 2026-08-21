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

        # 读取 preference
        item = store.get(namespace, "preference")
        print(f"读取preference结果: {item.value if item else None}")

        # 读取 a‑memory
        mem_item = store.get(namespace, "a-memory")
        print(f"读取a‑memory结果: {mem_item.value if mem_item else None}")

        # 搜索命名空间
        print("搜索命名空间:")
        items = store.search(namespace)
        for it in items:
            print(f"搜索结果 key={it.key}, value={it.value}")
