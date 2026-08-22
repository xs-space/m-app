import os

# from dotenv import load_dotenv
# load_dotenv()
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model=os.getenv("MODEL"),
    openai_api_key=os.getenv("API_KEY"),
    openai_api_base=os.getenv("BASE_URL"),
    model_provider="openai",
    temperature=0,
    max_retries=3,
    request_timeout=30,
    streaming=True,
)

resp = llm.stream("你好，帮我写一段python代码，计算1+1的结果，并打印出来。")
for chunk in resp:
    print(chunk.content, end="", flush=True)
