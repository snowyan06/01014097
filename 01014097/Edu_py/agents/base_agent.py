"""
Agent 基类
定义所有教育Agent的统一接口规范和通用能力

所有Agent应继承 BaseAgent 并实现 process() 方法
"""

import logging
from typing import Dict, Any, Optional
from adapters.llm_adapter import LLMAdapter, LLMConfig, LLMResponse

logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Agent 基类

    提供：
    - 统一的 LLM 适配器实例
    - 标准化的调用流程
    - 子类只需关注 prompt 构建和结果解析

    子类需实现:
        process() - 主处理方法
    """

    agent_name: str = "base"
    agent_description: str = "基础Agent"

    def __init__(self, adapter: Optional[LLMAdapter] = None, app_id: Optional[str] = None):
        """
        初始化Agent

        :param adapter: 外部传入的 LLMAdapter（可选，不传则自动创建）
        :param app_id: 该Agent专用的 app_id（可选，覆盖默认值）
        """
        self.adapter = adapter or LLMAdapter()
        self.app_id = app_id
        logger.info("[Agent:%s] 初始化完成", self.agent_name)

    def call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        通过适配器调用大模型（统一入口）

        :param prompt: 用户提示词
        :param system_prompt: 系统提示词
        :return: LLMResponse
        """
        logger.info("[Agent:%s] 开始调用LLM | prompt_len=%d", self.agent_name, len(prompt))
        response = self.adapter.call(
            prompt=prompt,
            system_prompt=system_prompt,
            app_id=self.app_id,
        )
        if response.success:
            logger.info("[Agent:%s] LLM调用成功 | response_len=%d", self.agent_name, len(response.content))
        else:
            logger.error("[Agent:%s] LLM调用失败 | error=%s", self.agent_name, response.error_message)
        return response

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        主处理方法（子类必须实现）

        :return: 标准化的结果字典 {"success": bool, "data": ..., "message": ...}
        """
        raise NotImplementedError(f"Agent '{self.agent_name}' 未实现 process() 方法")

    def _build_success_response(self, data: Any, message: str = "处理成功") -> Dict[str, Any]:
        """构建成功响应"""
        return {"success": True, "message": message, "data": data}

    def _build_error_response(self, message: str) -> Dict[str, Any]:
        """构建失败响应"""
        return {"success": False, "message": message, "data": None}
