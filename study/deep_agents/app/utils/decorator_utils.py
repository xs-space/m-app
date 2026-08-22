import time
import functools


def timer(func):
    """
    统计函数执行时间的装饰器
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper