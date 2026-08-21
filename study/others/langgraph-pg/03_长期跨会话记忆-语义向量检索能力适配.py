from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import IndexConfig

# 对话模型配置项
llm = ChatOpenAI(
    model="qwen3.8:27b",
    base_url="http://localhost:11433/v1",
    api_key="dummy",
    temperature=0.7,
    max_tokens=512,
)

# 向量嵌入模型配置项
embeddings = OpenAIEmbeddings(
    model="qwen3-embedding:8b",
    base_url="http://localhost:11433/v1",
    api_key="dummy",
)

index_config = IndexConfig(embeddings=embeddings, embed_path=["content"])

if __name__ == "__main__":
    store = InMemoryStore()

    user_id = "user_001"
    context = "chat"
    namespace = (user_id, context)

    store.put(namespace, "mem_1", {"content": "我平时主要用Python做分析"}, index=index_config)
    store.put(namespace, "mem_2", {"content": "我学习PostgreSQL，经常写SQL做数据表查询和统计"}, index=index_config)
    store.put(namespace, "mem_3", {"content": "周末喜欢爬山，户外运动，不喜欢宅在家"}, index=index_config)

    # 数据检索
    search_result = store.search(namespace, query="我想了解python相关知识", limit=1)

    # 打印检索结果
    for res in search_result:
        score_text = f"{res.score:.4f}" if res.score is not None else "N/A"
        print(f"key: {res.key}")
        print(f"相似度分数: {score_text}")
        print(f"记忆内容: {res.value}\n")
