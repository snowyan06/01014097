from http import HTTPStatus
from dashscope import Application
import os
import time
from requests.exceptions import ConnectionError, Timeout


def ai_learning_assistant(question: str, context: str) -> dict:
    """
    使用阿里云百炼模型，根据教学内容回答学生问题。

    参数：
        question (str): 学生提出的问题
        context (str): 当前课程的教学内容

    返回：
        dict: 包含 success、message 和 data 的结果字典
    """
    # 获取 API Key 和 App ID（优先从环境变量中获取）
    api_key = os.getenv('OTHER_API_KEY', 'sk-0fb559d546fc48668e6065f133f88413')
    app_id = os.getenv('APP_ID', 'fc3946fa969a4992bf35cda9233c524f')

    if not api_key or not app_id:
        return {
            "success": False,
            "message": "API_KEY 或 APP_ID 未配置，请设置环境变量 OTHER_API_KEY 和 APP_ID。",
            "data": None
        }

    # 最大重试次数
    max_retries = 3
    retry_delay = 2  # 秒

    for attempt in range(max_retries):
        try:
            print(f"收到问题：{question}")
            print(f"上下文：{context}")
            print(f"使用的 API Key: {api_key[:5]}...")
            print(f"使用的 App ID: {app_id}")
            print(f"正在调用百炼模型... (尝试 {attempt + 1}/{max_retries})")

            # 构建 Prompt，让 AI 结合教学内容回答问题
            full_prompt = f"""
请根据以下教学内容回答学生的问题。要求回答清晰、准确、符合教育场景。

教学内容：
{context}

学生问题：
{question}
"""

            # 调用百炼模型，添加超时设置
            response = Application.call(
                api_key=api_key,
                app_id=app_id,
                prompt=full_prompt,
                timeout=30  # 设置 30 秒超时
            )

            print(f"模型响应状态码：{response.status_code}")
            # 检查响应状态
            if response.status_code != HTTPStatus.OK:
                error_msg = f"请求失败：\n" \
                            f"request_id={response.request_id}\n" \
                            f"code={response.status_code}\n" \
                            f"message={response.message}\n" \
                            f"请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code "
                print(error_msg)

                # 如果是认证错误，不再重试
                if response.status_code in [401, 403]:
                    return {
                        "success": False,
                        "message": "API 密钥无效或权限不足，请检查 API_KEY 和 APP_ID 是否正确。",
                        "data": None
                    }

                # 其他错误继续重试
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                    continue

                return {
                    "success": False,
                    "message": error_msg,
                    "data": None
                }
            else:
                answer = response.output.text.strip()
                print(f"生成的回答：{answer[:50]}...")
                return {
                    "success": True,
                    "message": "回答已生成",
                    "data": {
                        "answer": answer,
                        "request_id": response.request_id
                    }
                }

        except (ConnectionError, Timeout) as e:
            print(f"网络连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}")

            # 如果是最后一次尝试，返回错误
            if attempt >= max_retries - 1:
                error_message = (
                    "网络连接失败，已尝试多次重试。\n"
                    "可能原因：\n"
                    "1. 网络连接不稳定\n"
                    "2. API 服务暂时不可用\n"
                    "3. 防火墙阻止了连接\n\n"
                    f"详细错误：{str(e)}"
                )
                print(error_message)
                return {
                    "success": False,
                    "message": error_message,
                    "data": None
                }

            # 等待后重试
            print(f"等待 {retry_delay}秒后重试...")
            time.sleep(retry_delay)
            retry_delay *= 2  # 指数退避

        except Exception as e:
            print(f"发生异常：{str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"发生异常：{str(e)}",
                "data": None
            }

    # 理论上不会到这里，但为了完整性
    return {
        "success": False,
        "message": "未知错误，请稍后重试",
        "data": None
    }
