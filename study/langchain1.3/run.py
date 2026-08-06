import os

from dotenv import load_dotenv
load_dotenv()

from utils.test_util import aa


print(os.getenv("DEEPSEEK_BASE_URL"))
print(aa)