"""
教师出题 Agent
迁移自 teacher_app.py，负责：
- 根据提示词生成考试题目
- 去掉了原文件的硬编码 API_KEY
"""

import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class QuestionGenAgent(BaseAgent):
    """教师出题 Agent"""

    agent_name: str = "question_gen"
    agent_description: str = "根据提示词生成考试题目"

    def __init__(self, adapter=None, app_id=None):
        super().__init__(adapter, app_id or settings.TEACHER_APP_ID or settings.APP_ID)

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        生成题目

        :param prompt: 用户指令，描述要生成的题目要求
        """
        prompt = kwargs.get("prompt")
        if not prompt:
            return self._build_error_response("缺少 prompt 参数")

        try:
            response = self.call_llm(prompt)

            if not response.success:
                return self._build_error_response(f"题目生成失败: {response.error_message}")

            return self._build_success_response(
                data={"question": response.content},
                message="题目生成成功"
            )

        except Exception as e:
            logger.error("[Agent:question_gen] 异常: %s", e, exc_info=True)
            return self._build_error_response(str(e))
