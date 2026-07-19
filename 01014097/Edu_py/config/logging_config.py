"""
统一日志配置
所有模块通过 setup_logging() 初始化日志，避免各文件重复配置
"""

import logging
import os
import sys


def setup_logging(level: str = None):
    """
    初始化全局日志配置

    :param level: 日志级别，默认从环境变量 LOG_LEVEL 读取，未设置则为 INFO
    """
    log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    if root_logger.handlers:
        root_logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler("edu_py.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)

    logging.info(f"日志系统初始化完成，级别: {log_level}")
