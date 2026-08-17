"""
collections
    主要特点
        高性能：底层 C 语言实现，性能优于纯 Python 实现
        针对性强：每个数据结构都解决一类特定问题
        集成度高：与 Python 内置类型和语法无缝衔接

    主要内容
        基础数据结构：
            Counter：是一个字典的子类，用于计数可哈希对象。
                核心方法：
                    elements()：返回一个迭代器，包含所有元素（按计数值重复）
                    most_common([n])：返回出现次数最多的 n 个元素及其计数
                    update()：更新计数（可以是另一个 Counter 或可迭代对象）
                    subtract()：减去计数（支持负数）
            defaultdict：带默认值的字典，访问不存在的键时，会自动创建一个默认值，避免 KeyError
                核心特性：
                    第一个参数是一个可调用对象（工厂函数），用于生成默认值
                    常见工厂函数：
                        int()：默认值为 0
                        list()：默认值为 []
                        dict()：默认值为 {}
                        set()：默认值为 set()
                        ...
            OrderedDict：有序字典，保持插入顺序。在 Python 3.7 及以上版本中，普通 dict 也保持插入顺序，但 OrderedDict 提供了额外的方法
                核心方法：
                    move_to_end(key, last=True)：将指定键移动到末尾或开头
                    popitem(last=True)：弹出最后一个或第一个键值对
            namedtuple：是一个工厂函数，用于创建具有命名字段的元组子类。它结合了元组的不可变性和字典的可读性
                核心特性：
                    字段可以通过名称访问，也可以通过索引访问
                    内存效率高，比普通类占用更少的内存
                    不可变，线程安全
            deque：双端队列，支持高效的两端插入和删除操作
        抽象基类：
            Iterable：可迭代对象的抽象基类
            Sequence：序列的抽象基类
            Mapping：映射的抽象基类
            ...
        高级数据结构：
        ChainMap：链式映射，支持多个字典的组合访问
        UserDict：用户自定义字典，继承自 dict 并可扩展
        UserList：用户自定义列表，继承自 list 并可扩展
        UserString：用户自定义字符串，继承自 str 并可扩展
"""

print("*" * 50, " Counter ", "*" * 50)
### Counter
from collections import Counter

# 1.基本计数
text = "hello world"
char_count = Counter(text)
print("基本计数：", char_count)
# 2.统计列表元素
numbers = ["apple", "banana", "banana", "orange", "orange", "orange"]
number_count = Counter(numbers)
print("列表元素统计：", number_count)
# 3.获取出现次数最多的元素
most_common = number_count.most_common(2)
print("出现次数最多的元素：", most_common)
# 4.元素迭代
print("元素迭代：", list(char_count.elements()))
# 5.数学运算
a = Counter(a=3, b=2)
b = Counter(a=1, b=2, c=3)
print("数学运算+：", a + b)
print("数学运算-：", a - b)
print("数学运算&：", a & b)  # 交集：取最小值
print("数学运算|：", a | b)  # 并集：取最大值
print("*" * 50, " defaultdict ", "*" * 50)

### defaultdict
from collections import defaultdict

# 1.分组（使用 list 作为默认值）
words = ["apple", "banana", "cherry", "date", "apricot", "blueberry"]
grouped = defaultdict(list)

for word in words:
    grouped[word[1]].append(word)
print("分组结果：", dict(grouped))
# 2.计数（使用 int 作为默认值）
text = "hello world"
counts = defaultdict(int)
for char in text:
    counts[char] += 1
print("计数结果：", dict(counts))
# 3.嵌套字典（使用 dict 作为默认值）
nested = defaultdict(dict)
nested["user1"]["name"] = "Alice"
nested["user1"]["age"] = 30
nested["user2"]["name"] = "Bob"
print("嵌套字典结果：", dict(nested))
print("*" * 50, " OrderedDict ", "*" * 50)

### OrderedDict
from collections import OrderedDict

# 1.基本使用
ordered = OrderedDict()
ordered["a"] = 1
ordered["b"] = 2
ordered["c"] = 3
print("有序字典：", dict(ordered))
# 2.移动元素
ordered.move_to_end("b")
print("移动元素后：", dict(ordered))
# 3.弹出元素
print("弹出元素：", ordered.popitem())
print("弹出元素：", ordered.popitem(last=False))
print("弹出元素后：", dict(ordered))
print("*" * 50, " namedtuple ", "*" * 50)

### namedtuple
from collections import namedtuple

# 1.定义和使用
UserInfo = namedtuple("UserInfo", ["username", "password"])
p = UserInfo("root", "123456")
print("命名元组：", p)
print("用户名：", p.username)
print("密码：", p.password)
# 2.转为字典
print("转为字典：", p._asdict())
# 3.替换字段
p2 = p._replace(password="654321")
print("替换字段后：", p2)
# 4.从序列或字典创建
p3 = UserInfo._make(["admin", "admin123"])
print("从序列创建：", p3)
p4 = UserInfo(**{"username": "guest", "password": "guest123"})
print("从字典创建：", p4)
# 5.应用场景：表示不可变数据对象
Person = namedtuple("Person", "name age gender")
alice = Person("Alice", 30, "Female")
bob = Person("Bob", 25, "Male")
bob = bob._replace(age=26)  # Bob 过生日了，年龄增加
print("Alice:", alice)
print("Bob:", bob)
