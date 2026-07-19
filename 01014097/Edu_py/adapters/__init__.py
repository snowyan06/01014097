"""
Edu_py 配置模块
统一管理环境变量、日志等全局配置
"""

from config.settings import settings, Settings

__all__ = ["settings", "Settings"]
"""
Edu_py 大模型适配器模块

提供统一的大模型调用接口，支持：
- 通义千问 DashScope（已实现）
- 讯飞星火 iFlytek Spark（预留骨架）
"""

from adapters.llm_adapter import LLMAdapter, LLMConfig, LLMResponse

__all__ = ["LLMAdapter", "LLMConfig", "LLMResponse"]
