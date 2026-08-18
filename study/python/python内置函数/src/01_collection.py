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
            deque：是一个双端队列，支持高效的两端高效地添加和删除元素。它的性能优于列表在两端的操作
                核心方法：
                    append(x)：在右侧添加元素
                    appendleft(x)：在左侧添加元素
                    pop()：从右侧弹出元素
                    popleft()：从左侧弹出元素
                    extend(iterable)：在右侧批量添加元素
                    extendleft(iterable)：在左侧批量添加元素（注意顺序会被反转）
                    rotate(n=1)：旋转队列 n 步，正数向右，负数向左
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
print("*" * 50, " deque ", "*" * 50)

### deque
from collections import deque

# 1.基本使用
dq = deque([1, 2, 3])
dq.append(4)  # 在右侧添加元素
dq.appendleft(0)  # 在左侧添加元素
print("双端队列：", dq)
print("从右侧弹出元素：", dq.pop())
print("从左侧弹出元素：", dq.popleft())
print("弹出元素后：", dq)
# 2.限制长度（用于实现固定大小的缓冲区）
buffer = deque(maxlen=3)
for i in range(5):
    buffer.append(i)
    print("缓冲区状态：", buffer)
# 3.旋转
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)  # 向右旋转 2 步
print("向右旋转后：", dq)
dq.rotate(-3)  # 向左旋转 3 步
print("向左旋转后：", dq)

print("*" * 50, " 案例一：词频统计与分析 ", "*" * 50)
### 案例一：词频统计与分析
# 需求：统计一段文本中每个单词的出现次数，并找出出现次数最多的前 10 个单词
import re
from collections import Counter


def word_frequency_analysis(text, top_n=10):
    """统计文本中单词的出现次数，并返回出现次数最多的前 top_n 个单词"""
    # 转换为小写并提取单词
    words = re.findall(r"\b\w+\b", text.lower())
    # 统计词频
    word_counts = Counter(words)
    # 获取出现次数最多的前 10 个单词
    return word_counts.most_common(top_n)


sample_text = """Python is a high-level, interpreted, general-purpose programming language. Python's design philosophy 
emphasizes code readability with its notable use of significant indentation. Python is dynamically-typed and 
garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional 
programming."""
print("出现次数最多的前 10 个单词：")
print(word_frequency_analysis(sample_text))

print("*" * 50, " 案例二：日志统计与分析 ", "*" * 50)
### 案例二：日志统计与分析
# 需求：分析一个 Web 服务器日志文件，统计每个客户端 Ip 的访问次数和请求的 URL 类型
from collections import defaultdict, Counter


def analyze_web_logs(log_lines):
    """分析 Web 服务器日志"""
    # 统计每个 IP 的访问次数
    ip_counts = Counter()
    # 统计每个 URL 的访问次数
    url_counts = Counter()
    # 统计每个状态码的出现次数
    status_counts = Counter()

    # 解析每一行日志（假设日志格式为：IP - - [日期] "请求方法 URL 协议" 状态码响应大小）
    for line in log_lines:
        parts = line.split()
        if len(parts) >= 10:
            ip = parts[0]
            request = parts[6]
            status = parts[8]

            ip_counts[ip] += 1
            url_counts[request] += 1
            status_counts[status] += 1

    return {"ip_counts": ip_counts, "url_counts": url_counts, "status_counts": status_counts}


# 示例日志数据
sample_logs = [
    '192.168.1.1 - - [01/Jan/2023:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.1.2 - - [01/Jan/2023:12:01:00 +0000] "GET /about.html HTTP/1.1" 200 512',
    '192.168.1.1 - - [01/Jan/2023:12:02:00 +0000] "POST /login HTTP/1.1" 302 0',
    '192.168.1.3 - - [01/Jan/2023:12:03:00 +0000] "GET /index.html HTTP/1.1" 200 1024',
    '192.168.1.2 - - [01/Jan/2023:12:04:00 +0000] "GET /contact.html HTTP/1.1" 404 256',
    '192.168.1.1 - - [01/Jan/2023:12:05:00 +0000] "GET /index.html HTTP/1.1" 200 1024',
]

# 执行分析
results = analyze_web_logs(sample_logs)
print("访问次数最多的 IP:")
for ip, count in results["ip_counts"].most_common(3):
    print(f"{ip}: {count} 次")
print("\n访问次数最多的 URL:")
for url, count in results["url_counts"].most_common(3):
    print(f"{url}: {count} 次")
print("\n状态码分布:")
for status, count in results["status_counts"].most_common():
    print(f"HTTP {status}: {count} 次")

print("*" * 50, " 案例三：任务调度与优先级队列 ", "*" * 50)
### 案例三：任务调度与优先级队列
# 需求：实现一个简单的任务调度系统，支持任务的添加、执行和优先级管理
from collections import deque, defaultdict
from dataclasses import dataclass, field


@dataclass(order=True)
class Task:
    """任务类，包含优先级、ID和描述"""

    priority: int
    task_id: int = field(compare=False)
    description: str = field(compare=False)


class TaskScheduler:
    """简单的任务调度器，使用优先级队列"""

    def __init__(self):
        # 使用 defaultdict 创建多个优先级队列
        self.queues = defaultdict(deque)
        self.task_counter = 0

    def add_task(self, description: str, priority: int = 0):
        """添加任务到指定优先级队列"""
        self.task_counter += 1
        task = Task(priority, self.task_counter, description)
        self.queues[priority].append(task)
        print(f"任务 '{description}' (ID: {self.task_counter}) 添加到优先级 {priority} 队列")

    def execute_next_task(self):
        """执行优先级最高的队列中的下一个任务"""
        if not self.queues:
            print("没有待执行的任务")
            return None

        # 获取最高优先级（数值最小表示优先级最高）
        highest_priority = min(self.queues.keys())
        queue = self.queues[highest_priority]

        if not queue:
            del self.queues[highest_priority]
            return self.execute_next_task()

        task = queue.popleft()
        print(f"执行任务 '{task.description}' (ID: {task.task_id}, 优先级: {task.priority})")

        # 如果队列为空，删除该优先级队列
        if not queue:
            del self.queues[highest_priority]

        return task

    def get_queue_status(self):
        """获取当前队列状态"""
        status = []
        for priority in sorted(self.queues.keys()):
            queue = self.queues[priority]
            status.append(f"优先级 {priority}: {len(queue)} 个任务")
        return "\n".join(status) if status else "队列为空"


# 使用示例
scheduler = TaskScheduler()

# 添加任务
scheduler.add_task("完成项目报告", priority=1)
scheduler.add_task("回复重要邮件", priority=0)
scheduler.add_task("参加团队会议", priority=2)
scheduler.add_task("修复紧急 Bug", priority=0)

print("\n当前队列状态:")
print(scheduler.get_queue_status())

print("\n执行任务:")
scheduler.execute_next_task()  # 执行优先级 0 的任务
scheduler.execute_next_task()  # 执行优先级 0 的下一个任务
scheduler.execute_next_task()  # 执行优先级 1 的任务

print("\n当前队列状态:")
print(scheduler.get_queue_status())

print("*" * 50, " 技能进阶 ", "*" * 50)
print("*" * 50, " 继承 UserDict, UserList, UserString ", "*" * 50)
# 示例：创建一个支持大小写不敏感查找的字典
from collections import UserDict


class CaseInsensitiveDict(UserDict):
    """大小写不敏感的字典"""

    def __setitem__(self, key, value):
        # 将键转换为小写存储
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        # 查找时也转换为小写
        return super().__getitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())


# 使用示例
cid = CaseInsensitiveDict()
cid["Name"] = "Alice"
cid["AGE"] = 25

print(cid["name"])  # Alice
print(cid["age"])  # 25
print("NAME" in cid)  # True
print(dict(cid))  # {'name': 'Alice', 'age': 25}

print("*" * 50, " 使用抽象基类 (ABCs) ", "*" * 50)
# 示例：创建一个自定义的序列类型
from collections.abc import Sequence


class MySequence(Sequence):
    """自定义序列类型，封装一个列表"""

    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"MySequence({self._data})"


# 使用示例
seq = MySequence([1, 2, 3, 4, 5])
# 继承了 Sequence 的所有方法
print(len(seq))  # 5
print(seq[2])  # 3
print(seq[1:4])  # [2, 3, 4]
print(3 in seq)  # True
print(list(reversed(seq)))  # [5, 4, 3, 2, 1]
# 类型检查
print(isinstance(seq, Sequence))  # True

print("*" * 50, " 内存优化 ", "*" * 50)
# 示例：使用 __slots__ 减少内存占用
from collections import namedtuple
import sys


# 使用普通类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# 使用 __slots__
class SlotPoint:
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y


# 使用 namedtuple
NTPoint = namedtuple("NTPoint", ["x", "y"])

# 创建实例并比较内存占用
p1 = Point(1, 2)
p2 = SlotPoint(1, 2)
p3 = NTPoint(1, 2)

print(f"普通类: {sys.getsizeof(p1)} 字节")
print(f"使用 __slots__: {sys.getsizeof(p2)} 字节")
print(f"namedtuple: {sys.getsizeof(p3)} 字节")

print("*" * 50, " 高级组合使用：ChainMap - 链接多个映射 ", "*" * 50)
# ChainMap 可以将多个字典或其他映射类型链接在一起，形成一个逻辑上的单一映射
# 示例：配置管理
from collections import ChainMap

# 配置来源
default_config = {"theme": "light", "font_size": 12, "notifications": True}
user_config = {"theme": "dark", "font_size": 14}
session_config = {"notifications": False}

# 创建 ChainMap（查找顺序：session_config -> user_config -> default_config）
config = ChainMap(session_config, user_config, default_config)

print(config["theme"])  # dark (来自 user_config)
print(config["font_size"])  # 14 (来自 user_config)
print(config["notifications"])  # False (来自 session_config)

# 修改只影响第一个映射
config["font_size"] = 16
print(config["font_size"])  # 16
print(user_config["font_size"])  # 14 (未改变)
print(session_config["font_size"])  # 16 (已改变)
print(default_config["font_size"])  # 16 (未改变)

print("*" * 50, " 高级组合使用：嵌套数据结构 ", "*" * 50)
# 示例：使用 defaultdict 和 deque 创建复杂的数据结构
from collections import defaultdict, deque, Counter


class SocialNetwork:
    """简单的社交网络模型"""

    def __init__(self):
        # 用户关系：key 是用户，value 是关注的用户集合
        self.following = defaultdict(set)
        # 用户动态：key 是用户，value 是动态队列
        self.posts = defaultdict(deque)
        # 兴趣标签：key 是用户，value 是标签计数器
        self.interests = defaultdict(Counter)

    def follow(self, user, target_user):
        """用户关注另一个用户"""
        self.following[user].add(target_user)
        print(f"{user} 开始关注 {target_user}")

    def post(self, user, content, tags=None):
        """用户发布动态"""
        if tags is None:
            tags = []

        post_id = len(self.posts[user]) + 1
        self.posts[user].appendleft((post_id, content, tags))  # 添加到队列左侧

        # 更新兴趣标签
        for tag in tags:
            self.interests[user][tag] += 1

        print(f"{user} 发布了新动态 (ID: {post_id}): {content}")

    def get_feed(self, user, limit=5):
        """获取用户的动态流（包括自己和关注的人的动态）"""
        feed = []

        # 添加自己的动态
        for post in self.posts[user]:
            feed.append((user, *post))
            if len(feed) >= limit:
                break

        # 添加关注用户的动态
        for followed_user in self.following[user]:
            for post in self.posts[followed_user]:
                feed.append((followed_user, *post))
                if len(feed) >= limit:
                    break
            if len(feed) >= limit:
                break

        # 按时间排序（假设 post_id 越大越新）
        feed.sort(key=lambda x: x[1], reverse=True)

        return feed[:limit]

    def get_top_interests(self, user, top_n=3):
        """获取用户的主要兴趣标签"""
        return self.interests[user].most_common(top_n)


# 使用示例
network = SocialNetwork()

# 添加用户和关系
network.follow("alice", "bob")
network.follow("alice", "charlie")
network.follow("bob", "charlie")

# 发布动态
network.post("alice", "今天学习了 Python collections 模块！", tags=["python", "编程", "学习"])
network.post("bob", "分享一个有趣的算法视频", tags=["算法", "视频", "技术"])
network.post("charlie", "参加了 Python 开发者大会", tags=["python", "会议", "技术"])
network.post("alice", "完成了一个小项目", tags=["python", "项目", "编程"])

# 获取动态流
print("\nAlice 的动态流:")
feed = network.get_feed("alice")
for user, post_id, content, tags in feed:
    print(f"{user} (动态 {post_id}): {content} [标签: {', '.join(tags)}]")

# 获取用户兴趣
print("\nAlice 的主要兴趣:")
for tag, count in network.get_top_interests("alice"):
    print(f"{tag}: {count} 次")
