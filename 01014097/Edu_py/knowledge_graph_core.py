import pymysql
import json
import time
from datetime import datetime
from openai import OpenAI
import os
import threading
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError
from typing import Optional, Dict, List

# 数据库配置（从环境变量获取更安全）
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'database': os.getenv('DB_NAME', 'mydb'),
    'charset': 'utf8mb4'
}

# 初始化 DashScope 客户端
client = OpenAI(
    api_key="sk-ws-H.EMELREX.LnYC.MEQCIAh-YVosP-8F7DPSyNIMFDsmrRTte6WCJAan124KtgYuAiAM8pxId4QTICSJsXQpvjb94ligb54deqouUpzN2y5xww",  # 直接使用新 Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def connect_db():
    """创建数据库连接"""
    return pymysql.connect(**db_config)


def analyze_question_content(question_content: str) -> Dict:
    """使用 AI 模型分析题目内容，提取知识点"""
    print("🔍 Analyzing question content:", question_content[:50] + "...")

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
- 1: 非常简单
- 2: 简单
- 3: 中等
- 4: 较难
- 5: 非常难

要求：
1. 准确识别题目涉及的所有知识点
2. 合理判断知识点类型和难度
3. 如果有依赖关系，明确指出父子关系
4. 只返回 JSON，不要其他解释文字
"""

    try:
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": "你是一个知识图谱构建助手，专门分析题目并提取知识点。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        response = completion.choices[0].message.content.strip()
        print("🤖 模型响应：", response)

        # 清理可能的 markdown 标记
        if response.startswith("json"): response = response[7:]
        if response.endswith("``"):
            response = response[:-3]
        response = response.strip()

        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败：{e}")
        print(f"原始响应：{response}")
        return {"knowledge_points": [], "dependencies": {}}
    except Exception as e:
        print("❌ 调用模型失败：", e)
        return {"knowledge_points": [], "dependencies": {}}


def knowledge_point_exists(knowledge_point: str, user_id: int) -> bool:
    """检查知识点是否存在"""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM knowledge_points WHERE name = %s AND user_id = %s"
            cursor.execute(sql, (knowledge_point, user_id))
            result = cursor.fetchone()
            return result[0] > 0
    finally:
        connection.close()


def save_knowledge_point(knowledge_point: str, user_id: int):
    """保存知识点"""
    if not knowledge_point_exists(knowledge_point, user_id):
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO knowledge_points (name, user_id) VALUES (%s, %s)"
                cursor.execute(sql, (knowledge_point, user_id))
                connection.commit()
        finally:
            connection.close()


def save_knowledge_dependency(parent: str, child: str, user_id: int):
    """保存知识点依赖关系"""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT IGNORE INTO knowledge_dependencies (parent, child, user_id)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (parent, child, user_id))
            connection.commit()
    finally:
        connection.close()


def save_knowledge_graph(knowledge_data: Dict, user_id: int):
    """保存整个知识图谱"""
    for point in knowledge_data.get("knowledge_points", []):
        if isinstance(point, dict):
            point_name = point.get("name")
        else:
            point_name = point
        if point_name:
            save_knowledge_point(point_name, user_id)

    for parent, children in knowledge_data.get("dependencies", {}).items():
        for child in children:
            save_knowledge_dependency(parent, child, user_id)


def update_user_knowledge_mastery(user_id: str, question_content: str, is_correct: bool):
    """根据答题情况更新用户知识点掌握度"""
    print(f"📊 更新用户 {user_id} 的知识点掌握度，答题正确：{is_correct}")

    knowledge_data = analyze_question_content(question_content)
    knowledge_points = knowledge_data.get("knowledge_points", [])

    if not knowledge_points:
        print("⚠️ 未提取到知识点，跳过掌握度更新")
        return

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            for kp_item in knowledge_points:
                if isinstance(kp_item, dict):
                    kp_name = kp_item.get("name")
                else:
                    kp_name = kp_item

                if not kp_name:
                    continue

                save_knowledge_point(kp_name, user_id)

                select_sql = """
                             SELECT total_questions, correct_count
                             FROM user_knowledge_mastery
                             WHERE user_id = %s AND knowledge_point_name = %s
                             """
                cursor.execute(select_sql, (user_id, kp_name))
                result = cursor.fetchone()

                if result:
                    total_questions = result[0] + 1
                    correct_count = result[1] + (1 if is_correct else 0)
                    mastery_score = (correct_count / total_questions) * 100

                    update_sql = """
                                 UPDATE user_knowledge_mastery
                                 SET total_questions = %s,
                                     correct_count = %s,
                                     mastery_score = %s,
                                     last_practice_time = NOW()
                                 WHERE user_id = %s AND knowledge_point_name = %s
                                 """
                    cursor.execute(update_sql, (
                        total_questions,
                        correct_count,
                        round(mastery_score, 2),
                        user_id,
                        kp_name
                    ))
                    print(f"✅ 更新知识点 '{kp_name}' 掌握度：{mastery_score:.2f}%")
                else:
                    total_questions = 1
                    correct_count = 1 if is_correct else 0
                    mastery_score = (correct_count / total_questions) * 100

                    insert_sql = """
                                 INSERT INTO user_knowledge_mastery
                                 (user_id, knowledge_point_name, mastery_score, total_questions, correct_count)
                                 VALUES (%s, %s, %s, %s, %s)
                                 """
                    cursor.execute(insert_sql, (
                        user_id,
                        kp_name,
                        round(mastery_score, 2),
                        total_questions,
                        correct_count
                    ))

                    print(f"✅ 新建知识点 '{kp_name}' 掌握度记录：{mastery_score:.2f}%")

            connection.commit()
    except Exception as e:
        print(f"❌ 更新掌握度失败：{e}")
        connection.rollback()
    finally:
        connection.close()


def get_user_knowledge_mastery(user_id: str, knowledge_point: str = None) -> Dict:
    """获取用户的知识点掌握度数据"""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if knowledge_point:
                sql = """
                      SELECT knowledge_point_name, mastery_score, total_questions,
                             correct_count, last_practice_time
                      FROM user_knowledge_mastery
                      WHERE user_id = %s AND knowledge_point_name = %s
                      """
                cursor.execute(sql, (user_id, knowledge_point))
            else:
                sql = """
                      SELECT knowledge_point_name, mastery_score, total_questions,
                             correct_count, last_practice_time
                      FROM user_knowledge_mastery
                      WHERE user_id = %s
                      ORDER BY mastery_score ASC
                      """
                cursor.execute(sql, (user_id,))

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
        print(f"❌ 获取掌握度数据失败：{e}")
        return {}
    finally:
        connection.close()


def get_knowledge_graph_from_db(user_id: Optional[int] = None) -> Dict:
    """从数据库获取知识图谱"""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if user_id:
                sql = """
                      SELECT kp1.name AS parent, kp2.name AS child
                      FROM knowledge_dependencies kd
                               JOIN knowledge_points kp1 ON kp1.name = kd.parent AND kp1.user_id = kd.user_id
                               JOIN knowledge_points kp2 ON kp2.name = kd.child AND kp2.user_id = kd.user_id
                      WHERE kd.user_id = %s
                      """
                cursor.execute(sql, (user_id,))
            else:
                sql = """
                      SELECT kp1.name AS parent, kp2.name AS child
                      FROM knowledge_dependencies kd
                               JOIN knowledge_points kp1 ON kp1.name = kd.parent AND kp1.user_id = kd.user_id
                               JOIN knowledge_points kp2 ON kp2.name = kd.child AND kp2.user_id = kd.user_id
                      """
                cursor.execute(sql)

            results = cursor.fetchall()
            graph = {}
            for parent, child in results:
                if parent not in graph:
                    graph[parent] = []
                graph[parent].append(child)
            return graph
    finally:
        connection.close()


class DBChangeListener:
    """数据库变更监听器"""

    def __init__(self, db_config: Dict, interval: int = 5):
        self.db_config = db_config
        self.interval = interval
        self.last_id = self.get_max_answer_id()
        self.running = False

    def get_max_answer_id(self) -> int:
        """获取当前最大答案 ID"""
        conn = None
        try:
            conn = connect_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM user_answers")
                result = cursor.fetchone()
                return result[0] or 0
        except OperationalError as e:
            print(f"Database error: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    def check_new_answers(self):
        """检查新答案"""
        conn = None
        try:
            conn = connect_db()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, question_content, user_id, is_correct
                    FROM user_answers
                    WHERE user_id = 26
                    ORDER BY id ASC
                """)

                new_answers = cursor.fetchall()
                if new_answers:
                    print(f"发现 {len(new_answers)} 条新答题记录")
                    for answer in new_answers:
                        self.process_answer(answer)
                    self.last_id = new_answers[-1]['id']

        except OperationalError as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def process_answer(self, answer: Dict):
        """处理单个答案"""
        print(f"处理答题记录 ID: {answer['id']}")
        try:
            knowledge_data = analyze_question_content(answer['question_content'])
            save_knowledge_graph(knowledge_data, answer['user_id'])

            is_correct = answer.get('is_correct', True)
            update_user_knowledge_mastery(answer['user_id'], answer['question_content'], is_correct)

            print(f"成功处理答题记录 ID: {answer['id']}")
        except Exception as e:
            print(f"处理答题记录 ID: {answer['id']} 时出错：{e}")

    def start(self):
        """启动监听器"""
        self.running = True
        print("启动数据库监听器...")
        
        # 新增：首次启动时处理所有历史数据
        print("正在初始化历史答题记录...")
        conn = None
        try:
            conn = connect_db()
            with conn.cursor(DictCursor) as cursor:
                # 获取所有未处理的答题记录
                cursor.execute("""
                    SELECT id, question_content, user_id, is_correct
                    FROM user_answers
                    ORDER BY id ASC
                """)
                all_answers = cursor.fetchall()
                
                if all_answers:
                    print(f"发现 {len(all_answers)} 条历史答题记录，开始处理...")
                    for idx, answer in enumerate(all_answers, 1):
                        print(f"[{idx}/{len(all_answers)}] 处理答题记录 ID: {answer['id']}")
                        try:
                            # 分析题目并保存知识图谱
                            knowledge_data = analyze_question_content(answer['question_content'])
                            save_knowledge_graph(knowledge_data, answer['user_id'])
                            
                            # 更新掌握度
                            is_correct = answer.get('is_correct', 1)
                            update_user_knowledge_mastery(answer['user_id'], answer['question_content'], is_correct)
                            
                            print(f"✅ 成功处理答题记录 ID: {answer['id']}")
                        except Exception as e:
                            print(f"❌ 处理答题记录 ID: {answer['id']} 时出错：{e}")
                    
                    print("✅ 历史数据处理完成！")
                else:
                    print("ℹ️ 没有历史答题记录")
        except Exception as e:
            print(f"❌ 初始化历史数据失败：{e}")
        finally:
            if conn:
                conn.close()
        
        # 启动定时检查
        while self.running:
            self.check_new_answers()
            time.sleep(self.interval)

    def stop(self):
        """停止监听器"""
        self.running = False
        print("停止数据库监听器")
