"""
日志工具模块 - 基于 loguru
"""

import sys
from loguru import logger

# 移除默认的日志处理器
logger.remove()

# 配置日志格式
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# 添加控制台输出
logger.add(
    sys.stderr,
    level="DEBUG",
    format=LOG_FORMAT,
    colorize=True,
)

# # 添加文件输出 - 按天轮转
# logger.add(
#     "logs/app_{time:YYYY-MM-DD}.log",
#     rotation="00:00",       # 每天午夜轮转
#     retention="30 days",    # 保留30天
#     compression="zip",      # 压缩旧日志
#     level="DEBUG",
#     format=LOG_FORMAT,
#     encoding="utf-8",
# )

# 添加错误日志单独输出
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="90 days",
    compression="zip",
    level="ERROR",
    format=LOG_FORMAT,
    encoding="utf-8",
)


def get_logger():
    """获取 logger 实例"""
    return logger


# 便捷方法
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
