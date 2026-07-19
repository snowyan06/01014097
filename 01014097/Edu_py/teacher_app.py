import os
from http import HTTPStatus
from dashscope import Application

# 设置 API Key 和 App ID（从环境变量获取）
API_KEY = os.getenv('OTHER_API_KEY', 'sk-10eea048e8244237b67db0e87a590cd3')
APP_ID = os.getenv('TEACHER_APP_ID', 'f0a9c988fe224e95bdadc380a6b5ed29')  # 替换为你的应用/智能体 ID

def generate_question(prompt: str):
    """
    调用 DashScope 平台上的 AI 智能体生成题目
    :param prompt: 用户指令，描述要生成的题目要求
    :return: AI 生成的题目内容
    """
    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt
        )

        if response.status_code != HTTPStatus.OK:
            print(f'请求失败，状态码：{response.status_code}')
            print(f'错误信息：{response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code ')
            return None

        # 成功返回结果
        return response.output.text

    except Exception as e:
        print(f'调用异常：{str(e)}')
        return None


if __name__ == "__main__":
    # 示例提示词：告诉 AI 要生成什么类型的题目
    user_prompt = """
    请为《嵌入式Linux开发实践教程》第3章“交叉编译环境搭建”生成一道选择题。
    """

    # 调用 AI 生成题目
    question = generate_question(user_prompt)

    if question:
        print("✅ AI 生成的题目如下：")
        print(question)
    else:
        print("❌ 题目生成失败，请检查网络或API设置。")