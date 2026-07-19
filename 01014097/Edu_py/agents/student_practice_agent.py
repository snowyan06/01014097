"""
学生练习 Agent
迁移自 student_app.py，负责：
- 学生端出题
- 学生端自动批改
"""

import json
import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class StudentPracticeAgent(BaseAgent):
    """学生练习 Agent"""

    agent_name: str = "student_practice"
    agent_description: str = "学生端出题与自动批改"

    def __init__(self, adapter=None, app_id=None):
        super().__init__(adapter, app_id or settings.STUDENT_APP_ID or settings.APP_ID)

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        统一入口，根据 action 分发

        :param action: "generate" | "grade"
        """
        action = kwargs.get("action", "generate")

        if action == "generate":
            return self.generate_question(**kwargs)
        elif action == "grade":
            return self.grade_answer(**kwargs)
        else:
            return self._build_error_response(f"不支持的 action: {action}")

    def generate_question(self, **kwargs) -> Dict[str, Any]:
        """学生端出题"""
        prompt = kwargs.get("prompt")
        if not prompt:
            return self._build_error_response("缺少 prompt 参数")

        try:
            response = self.call_llm(prompt)

            if not response.success:
                return self._build_error_response(f"题目生成失败: {response.error_message}")

            return self._build_success_response(
                data={"questions": response.content},
                message="题目生成成功"
            )

        except Exception as e:
            logger.error("[Agent:student_practice] 出题异常: %s", e, exc_info=True)
            return self._build_error_response(str(e))

    def grade_answer(self, **kwargs) -> Dict[str, Any]:
        """自动批改"""
        question = kwargs.get("question")
        student_answer = kwargs.get("student_answer")
        question_type = kwargs.get("question_type", "未知")

        if not question or not student_answer:
            return self._build_error_response("缺少 question 或 student_answer 参数")

        prompt = f"""
你是一位嵌入式Linux教学助手，请根据以下题目和学生作答进行评分和反馈：

题目：
{question}

题型：
{question_type}

学生作答：
{student_answer}
"""
        try:
            response = self.call_llm(prompt)

            if not response.success:
                return self._build_error_response("批改失败")

            result_str = response.content.replace("```json", "").replace("```", "").strip()

            try:
                result = json.loads(result_str)
                return self._build_success_response(data=result, message="批改完成")
            except json.JSONDecodeError as je:
                logger.error("[Agent:student_practice] JSON 解析失败: %s", je)
                return self._build_error_response("JSON 解析失败")

        except Exception as e:
            logger.error("[Agent:student_practice] 批改异常: %s", e, exc_info=True)
            return self._build_error_response(str(e))
