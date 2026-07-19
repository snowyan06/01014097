import json
import os
from http import HTTPStatus
from dashscope import Application, Generation

# 设置 API Key 和 App ID（从环境变量获取）
API_KEY = os.getenv('OTHER_API_KEY', 'sk-10eea048e8244237b67db0e87a590cd3')
APP_ID = os.getenv('STUDENT_APP_ID', '2fca67c39561433a92b8d2667ec510e6')  # 替换为你自己的应用ID

# ========================
# 模块1：AI 出题模块
# ========================

def generate_question_stu(prompt: str):
    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt
        )

        if response.status_code != HTTPStatus.OK:
            print(f'请求失败，状态码：{response.status_code}')
            print(f'错误信息：{response.message}')
            return None

        # 假设返回的是结构化题目内容
        return response.output.text

    except Exception as e:
        print(f'调用异常：{str(e)}')
        return None


# ========================
# 模块2：AI 批改模块
# ========================
def grade_answer(question, student_answer, question_type):
    """
    使用 Application.call 调用 DashScope AI Agent 进行智能批改
    :param question: 题目内容（题型｜题干）
    :param student_answer: 学生输入的答案
    :return: JSON 格式的批改结果
    """

    # 自动提取题型（假设题目格式为“题型｜题干”）
    # question_type = question.split('|')[0].strip() if '|' in question else "未知"

    # 构造 Prompt 提示词
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
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt
        )

        if response.status_code == HTTPStatus.OK:
            result_str = response.output.text.strip()
            result_str = result_str.replace("```json", "").replace("```", "")

            # ✅ 使用 json.loads 解析
            try:
                return json.loads(result_str)
            except json.JSONDecodeError as je:
                print(f"JSON 解析失败：{je}")
                return {"error": "JSON 解析失败"}

        else:
            print(f"批改失败，状态码：{response.status_code}")
            print(response.message)
            return {"error": "批改失败"}

    except Exception as e:
        print(f"批改调用异常：{e}")
        return {"error": str(e)}

# ========================
# 示例运行主程序
# ========================

if __name__ == "__main__":
    # Step 1: 生成题目
    user_prompt = """
    请为《嵌入式Linux开发实践教程》第3章“交叉编译环境搭建”生成一道选择题。
    """

    raw_questions = generate_question_stu(user_prompt)

    if not raw_questions:
        print("❌ 题目生成失败，请检查网络或API设置。")
    else:
        print("\n📘【实时练习评测助手】")
        print("👇 已生成以下题目：\n")
        print(raw_questions)

        lines = raw_questions.strip().split('\n')
        questions = []

        for line in lines[1:]:  # 跳过表头
            line = line.strip()
            if not line:
                continue  # 跳过空行

            parts = line.split('|')  # 改为英文竖线
            if len(parts) >= 3:
                q_type, content, difficulty = parts
                full_question = f"{q_type}|{content}|{difficulty}"
                questions.append(full_question)
            else:
                print(f"⚠️ 题目格式不正确：{line}")

        # Step 3: 学生答题模拟
        for question in questions:
            print("\n📝 请作答以下题目：")
            print(question)
            student_answer = input("请输入你的答案：").strip()

            # Step 4: 自动批改（不需要传入正确答案）
            grading_result = grade_answer(question, student_answer)

            print("\n🔍 批改结果如下：")
            if "error" in grading_result:
                print("❌ 批改服务异常，请稍后再试。")
            else:
                print(f"是否正确：{'✅' if grading_result['correct'] else '❌'}")
                print(f"你的答案：{grading_result['student_answer']}")
                print(f"正确答案：{grading_result['correct_answer']}")
                print(f"教学解析：{grading_result['feedback']}")