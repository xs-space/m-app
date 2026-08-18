import json

import jsonpath

# 读取 JSON 文件并转为字典
with open("jsonpath/test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

code = jsonpath.jsonpath(data, "$.code")
print(code)
# result = jsonpath.jsonpath(data, "$.result")
# print(result)
productName = jsonpath.jsonpath(data, "$..productName")  # 相对路径下所有的productName
print(productName)
item1 = jsonpath.jsonpath(data, "$.result.0")  # 中括号和点都可以
print(item1)
item2 = jsonpath.jsonpath(data, "$.result[0]")
print(item2)
productName1 = jsonpath.jsonpath(data, "$.result.0.productName")
print(productName1)
# 带条件筛选 id=1209560807 的name
productName2 = jsonpath.jsonpath(data, "$.result[?(@.productId == 1209560807)].productName")
print(productName2)
