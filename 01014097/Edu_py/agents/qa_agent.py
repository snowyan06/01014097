"""
问答答疑 Agent
迁移自 answer.py，负责：
- 根据教学内容回答学生问题
"""

import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class QAAgent(BaseAgent):
    """问答答疑 Agent"""

    agent_name: str = "qa"
    agent_description: str = "根据教学内容回答学生问题"

    def __init__(self, adapter=None, app_id=None):
        super().__init__(adapter, app_id or settings.APP_ID)

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        回答学生问题

        :param question: 学生问题
        :param context: 教学内容上下文
        """
        question = kwargs.get("question")
        context = kwargs.get("context", "")

        if not question:
            return self._build_error_response("缺少 question 参数")

        full_prompt = f"""
请根据以下教学内容回答学生的问题。要求回答清晰、准确、符合教育场景。

教学内容：
{context}

学生问题：
{question}
"""
        try:
            response = self.call_llm(full_prompt)

            if not response.success:
                return self._build_error_response(f"回答生成失败: {response.error_message}")

            return self._build_success_response(
                data={
                    "answer": response.content,
                    "request_id": response.request_id
                },
                message="回答已生成"
            )

        except Exception as e:
            logger.error("[Agent:qa] 异常: %s", e, exc_info=True)
            return self._build_error_response(f"发生异常：{str(e)}")
