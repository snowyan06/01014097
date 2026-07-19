"""
知识图谱 Agent
迁移自 knowledge_graph_core.py，负责：
- 分析题目内容，提取知识点及依赖关系
- 保存知识图谱到数据库
- 更新用户知识点掌握度
- 数据库变更监听器（DBChangeListener）

注意：此 Agent 使用 OpenAI 兼容模式调用（call_with_messages）
"""

import json
import time
import logging
from typing import Dict, Any, Optional, List

import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError

from agents.base_agent import BaseAgent
from adapters.llm_adapter import LLMAdapter, LLMConfig
from config.settings import settings

logger = logging.getLogger(__name__)


class KnowledgeGraphAgent(BaseAgent):
    """知识图谱 Agent"""

    agent_name: str = "knowledge_graph"
    agent_description: str = "分析题目提取知识点，构建知识图谱并跟踪掌握度"

    def __init__(self, adapter=None, app_id=None):
        if adapter is None:
            adapter = LLMAdapter(LLMConfig(
                provider=settings.LLM_PROVIDER,
                api_key=settings.DASH_SCOPE_API_KEY or settings.API_KEY,
                model=settings.LLM_MODEL,
            ))
        super().__init__(adapter, app_id)

    # ================================================================
    # AI 分析
    # ================================================================

    def analyze_question_content(self, question_content: str) -> Dict:
        """使用 AI 分析题目内容，提取知识点"""
        logger.info("[Agent:knowledge_graph] 分析题目: %s...", question_content[:50])

        prompt = f"""
你是一个知识图谱构建助手。请分析以下题目内容，提取涉及的知识点以及它们之间的依赖关系。

题目内容：
{question_content}

请严格按照以下 JSON 格式返回：
{{
  "knowledge_points": [
    {{
      "name": "知识点名称",
      "category": "core|branch|leaf",
      "difficulty": 1-5
    }}
  ],
  "dependencies": {{
    "父知识点名称": ["子知识点 1", "子知识点 2"]
  }}
}}

分类说明：
- core: 核心知识点（基础概念，多个知识点的前置条件）
- branch: 分支知识点（承上启下，连接多个知识体系）
- leaf: 应用知识点（具体应用，需要前置知识支撑）

难度说明：
- 1: 非常简单  2: 简单  3: 中等  4: 较难  5: 非常难

要求：
1. 准确识别题目涉及的所有知识点
2. 合理判断知识点类型和难度
3. 如果有依赖关系，明确指出父子关系
4. 只返回 JSON，不要其他解释文字
"""
        messages = [
            {"role": "system", "content": "你是一个知识图谱构建助手，专门分析题目并提取知识点。"},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.adapter.call_with_messages(messages, temperature=0.3, max_tokens=2000)

            if not response.success:
                logger.error("[Agent:knowledge_graph] LLM 调用失败: %s", response.error_message)
                return {"knowledge_points": [], "dependencies": {}}

            raw = response.content
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error("[Agent:knowledge_graph] JSON 解析失败: %s", e)
            return {"knowledge_points": [], "dependencies": {}}
        except Exception as e:
            logger.error("[Agent:knowledge_graph] 调用模型失败: %s", e)
            return {"knowledge_points": [], "dependencies": {}}

    # ================================================================
    # 数据库操作
    # ================================================================

    @staticmethod
    def _connect_db():
        return pymysql.connect(**settings.get_db_config())

    def _knowledge_point_exists(self, knowledge_point: str, user_id: int) -> bool:
        conn = self._connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM knowledge_points WHERE name = %s AND user_id = %s",
                    (knowledge_point, user_id)
                )
                return cursor.fetchone()[0] > 0
        finally:
            conn.close()

    def _save_knowledge_point(self, knowledge_point: str, user_id: int):
        if not self._knowledge_point_exists(knowledge_point, user_id):
            conn = self._connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO knowledge_points (name, user_id) VALUES (%s, %s)",
                        (knowledge_point, user_id)
                    )
                    conn.commit()
            finally:
                conn.close()

    def _save_knowledge_dependency(self, parent: str, child: str, user_id: int):
        conn = self._connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT IGNORE INTO knowledge_dependencies (parent, child, user_id) VALUES (%s, %s, %s)",
                    (parent, child, user_id)
                )
                conn.commit()
        finally:
            conn.close()

    def save_knowledge_graph(self, knowledge_data: Dict, user_id: int):
        """保存整个知识图谱"""
        for point in knowledge_data.get("knowledge_points", []):
            point_name = point.get("name") if isinstance(point, dict) else point
            if point_name:
                self._save_knowledge_point(point_name, user_id)

        for parent, children in knowledge_data.get("dependencies", {}).items():
            for child in children:
                self._save_knowledge_dependency(parent, child, user_id)

    def update_user_knowledge_mastery(self, user_id: str, question_content: str, is_correct: bool):
        """根据答题情况更新用户知识点掌握度"""
        logger.info("[Agent:knowledge_graph] 更新用户 %s 掌握度，答题正确: %s", user_id, is_correct)

        knowledge_data = self.analyze_question_content(question_content)
        knowledge_points = knowledge_data.get("knowledge_points", [])

        if not knowledge_points:
            logger.warning("未提取到知识点，跳过掌握度更新")
            return

        conn = self._connect_db()
        try:
            with conn.cursor() as cursor:
                for kp_item in knowledge_points:
                    kp_name = kp_item.get("name") if isinstance(kp_item, dict) else kp_item
                    if not kp_name:
                        continue

                    self._save_knowledge_point(kp_name, user_id)

                    cursor.execute(
                        "SELECT total_questions, correct_count FROM user_knowledge_mastery WHERE user_id = %s AND knowledge_point_name = %s",
                        (user_id, kp_name)
                    )
                    result = cursor.fetchone()

                    if result:
                        total_questions = result[0] + 1
                        correct_count = result[1] + (1 if is_correct else 0)
                        mastery_score = (correct_count / total_questions) * 100
                        cursor.execute(
                            """UPDATE user_knowledge_mastery
                               SET total_questions = %s, correct_count = %s,
                                   mastery_score = %s, last_practice_time = NOW()
                               WHERE user_id = %s AND knowledge_point_name = %s""",
                            (total_questions, correct_count, round(mastery_score, 2), user_id, kp_name)
                        )
                    else:
                        correct_count = 1 if is_correct else 0
                        mastery_score = (correct_count / 1) * 100
                        cursor.execute(
                            """INSERT INTO user_knowledge_mastery
                               (user_id, knowledge_point_name, mastery_score, total_questions, correct_count)
                               VALUES (%s, %s, %s, %s, %s)""",
                            (user_id, kp_name, round(mastery_score, 2), 1, correct_count)
                        )

                conn.commit()
        except Exception as e:
            logger.error("[Agent:knowledge_graph] 更新掌握度失败: %s", e)
            conn.rollback()
        finally:
            conn.close()

    # ================================================================
    # 查询方法（供 main.py 路由直接调用）
    # ================================================================

    @staticmethod
    def get_knowledge_graph_from_db(user_id: Optional[int] = None) -> Dict:
        conn = KnowledgeGraphAgent._connect_db()
        try:
            with conn.cursor() as cursor:
                if user_id:
                    cursor.execute(
                        """SELECT kp1.name AS parent, kp2.name AS child
                           FROM knowledge_dependencies kd
                           JOIN knowledge_points kp1 ON kp1.name = kd.parent AND kp1.user_id = kd.user_id
                           JOIN knowledge_points kp2 ON kp2.name = kd.child AND kp2.user_id = kd.user_id
                           WHERE kd.user_id = %s""",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        """SELECT kp1.name AS parent, kp2.name AS child
                           FROM knowledge_dependencies kd
                           JOIN knowledge_points kp1 ON kp1.name = kd.parent AND kp1.user_id = kd.user_id
                           JOIN knowledge_points kp2 ON kp2.name = kd.child AND kp2.user_id = kd.user_id"""
                    )

                results = cursor.fetchall()
                graph = {}
                for parent, child in results:
                    if parent not in graph:
                        graph[parent] = []
                    graph[parent].append(child)
                return graph
        finally:
            conn.close()

    @staticmethod
    def get_user_knowledge_mastery(user_id: str, knowledge_point: str = None) -> Dict:
        conn = KnowledgeGraphAgent._connect_db()
        try:
            with conn.cursor() as cursor:
                if knowledge_point:
                    cursor.execute(
                        """SELECT knowledge_point_name, mastery_score, total_questions,
                                  correct_count, last_practice_time
                           FROM user_knowledge_mastery
                           WHERE user_id = %s AND knowledge_point_name = %s""",
                        (user_id, knowledge_point)
                    )
                else:
                    cursor.execute(
                        """SELECT knowledge_point_name, mastery_score, total_questions,
                                  correct_count, last_practice_time
                           FROM user_knowledge_mastery
                           WHERE user_id = %s ORDER BY mastery_score ASC""",
                        (user_id,)
                    )

                results = cursor.fetchall()
                mastery_data = {}
                for row in results:
                    mastery_data[row[0]] = {
                        'mastery_score': float(row[1]) if row[1] else 0,
                        'total_questions': row[2],
                        'correct_count': row[3],
                        'last_practice_time': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
                    }
                return mastery_data
        except Exception as e:
            logger.error("获取掌握度数据失败: %s", e)
            return {}
        finally:
            conn.close()

    # ================================================================
    # 主处理方法
    # ================================================================

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        分析题目并更新知识图谱

        :param question_content: 题目内容
        :param user_id: 用户 ID
        :param is_correct: 是否答对
        """
        question_content = kwargs.get("question_content")
        user_id = kwargs.get("user_id")
        is_correct = kwargs.get("is_correct", True)

        if not question_content or not user_id:
            return self._build_error_response("缺少 question_content 或 user_id 参数")

        try:
            knowledge_data = self.analyze_question_content(question_content)
            self.save_knowledge_graph(knowledge_data, user_id)
            self.update_user_knowledge_mastery(user_id, question_content, is_correct)

            return self._build_success_response(
                data={"knowledge_data": knowledge_data},
                message="知识图谱更新成功"
            )
        except Exception as e:
            logger.error("[Agent:knowledge_graph] 异常: %s", e, exc_info=True)
            return self._build_error_response(str(e))


# ================================================================
# 数据库变更监听器（保持全局可用）
# ================================================================

class DBChangeListener:
    """数据库变更监听器 - 监听新答题记录并自动更新知识图谱"""

    def __init__(self, interval: int = 5):
        self.interval = interval
        self.running = False
        self.agent = KnowledgeGraphAgent()

    def _connect_db(self):
        return pymysql.connect(**settings.get_db_config())

    def get_max_answer_id(self) -> int:
        conn = None
        try:
            conn = self._connect_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM user_answers")
                result = cursor.fetchone()
                return result[0] or 0
        except OperationalError as e:
            logger.error("Database error: %s", e)
            return 0
        finally:
            if conn:
                conn.close()

    def check_new_answers(self):
        conn = None
        try:
            conn = self._connect_db()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, question_content, user_id, is_correct
                    FROM user_answers
                    WHERE user_id = 26
                    ORDER BY id ASC
                """)
                new_answers = cursor.fetchall()
                if new_answers:
                    logger.info("发现 %d 条新答题记录", len(new_answers))
                    for answer in new_answers:
                        self._process_answer(answer)
        except OperationalError as e:
            logger.error("Database error: %s", e)
        finally:
            if conn:
                conn.close()

    def _process_answer(self, answer: Dict):
        logger.info("处理答题记录 ID: %s", answer['id'])
        try:
            knowledge_data = self.agent.analyze_question_content(answer['question_content'])
            self.agent.save_knowledge_graph(knowledge_data, answer['user_id'])

            is_correct = answer.get('is_correct', True)
            self.agent.update_user_knowledge_mastery(answer['user_id'], answer['question_content'], is_correct)

            logger.info("成功处理答题记录 ID: %s", answer['id'])
        except Exception as e:
            logger.error("处理答题记录 ID: %s 时出错: %s", answer['id'], e)

    def start(self):
        """启动监听器（首次处理全部历史数据，然后轮询）"""
        self.running = True
        logger.info("启动数据库监听器...")

        conn = None
        try:
            conn = self._connect_db()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, question_content, user_id, is_correct
                    FROM user_answers ORDER BY id ASC
                """)
                all_answers = cursor.fetchall()

                if all_answers:
                    logger.info("发现 %d 条历史答题记录，开始处理...", len(all_answers))
                    for idx, answer in enumerate(all_answers, 1):
                        try:
                            knowledge_data = self.agent.analyze_question_content(answer['question_content'])
                            self.agent.save_knowledge_graph(knowledge_data, answer['user_id'])
                            is_correct = answer.get('is_correct', 1)
                            self.agent.update_user_knowledge_mastery(answer['user_id'], answer['question_content'], is_correct)
                            logger.info("[%d/%d] 处理答题记录 ID: %s", idx, len(all_answers), answer['id'])
                        except Exception as e:
                            logger.error("处理答题记录 ID: %s 时出错: %s", answer['id'], e)
                    logger.info("历史数据处理完成！")
                else:
                    logger.info("没有历史答题记录")
        except Exception as e:
            logger.error("初始化历史数据失败: %s", e)
        finally:
            if conn:
                conn.close()

        while self.running:
            self.check_new_answers()
            time.sleep(self.interval)

    def stop(self):
        """停止监听器"""
        self.running = False
        logger.info("停止数据库监听器")
