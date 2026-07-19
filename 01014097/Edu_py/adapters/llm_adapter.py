"""
通用大模型适配器
统一封装：API请求构建、参数校验、异常捕获、超时重试、日志打印

当前支持：
- 通义千问 DashScope Application API（已实现）
- 通义千问 OpenAI 兼容模式（已实现，用于 knowledge_graph 等场景）
- 讯飞星火 iFlytek Spark（预留骨架）

使用方式:
    from adapters import LLMAdapter, LLMConfig

    # 方式1：自动从环境变量加载配置
    adapter = LLMAdapter()
    response = adapter.call("请回答这个问题...")

    # 方式2：手动指定配置
    config = LLMConfig(provider="dashscope", api_key="xxx", app_id="yyy")
    adapter = LLMAdapter(config)
    response = adapter.call("请回答这个问题...")

    if response.success:
        print(response.content)
    else:
        print(f"调用失败: {response.error_message}")
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from http import HTTPStatus
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """统一的大模型响应模型"""
    success: bool
    content: str = ""
    error_message: str = ""
    request_id: str = ""
    usage: Dict[str, int] = field(default_factory=dict)
    raw_response: Any = None


@dataclass
class LLMConfig:
    """大模型调用配置"""
    provider: str = "dashscope"
    api_key: str = ""
    app_id: str = ""
    model: str = "qwen-turbo"
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 2.0
    temperature: float = 0.7
    max_tokens: int = 2000


class LLMAdapter:
    """
    通用大模型适配器

    功能特性：
    - 统一调用接口，屏蔽不同 LLM 提供商的差异
    - 自动重试（指数退避）
    - 完善的异常捕获和日志记录
    - 参数校验（prompt非空、配置合法性）
    - 支持 Application API 和 OpenAI 兼容模式两种调用方式
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._load_default_config()
        self._validate_config()

    def _load_default_config(self) -> LLMConfig:
        """从环境变量加载默认配置"""
        return LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "dashscope"),
            api_key=os.getenv("OTHER_API_KEY", ""),
            app_id=os.getenv("APP_ID", ""),
            model=os.getenv("LLM_MODEL", "qwen-turbo"),
            timeout=int(os.getenv("LLM_TIMEOUT", "30")),
            max_retries=int(os.getenv("LLM_MAX_RETRIES", "3")),
        )

    def _validate_config(self):
        """参数校验，确保配置合法"""
        if not self.config.api_key:
            raise ValueError("API_KEY 未配置，请设置环境变量 OTHER_API_KEY 或传入 LLMConfig")
        if self.config.max_retries < 0:
            raise ValueError("max_retries 不能为负数")
        if self.config.timeout <= 0:
            raise ValueError("timeout 必须大于 0")

    # ================================================================
    # 公开调用接口
    # ================================================================

    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        app_id: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        统一调用入口（Application API 模式，自动重试 + 异常捕获 + 日志）

        :param prompt: 用户提示词
        :param system_prompt: 系统提示词（可选，拼接在 prompt 前面）
        :param app_id: 覆盖默认 app_id（可选，不同Agent可能用不同app_id）
        :param temperature: 温度参数（预留，Application API 暂不支持）
        :param max_tokens: 最大token数（预留，Application API 暂不支持）
        :return: LLMResponse
        """
        if not prompt or not prompt.strip():
            return LLMResponse(success=False, error_message="prompt 不能为空")

        retry_delay = self.config.retry_delay
        last_error = ""

        for attempt in range(1, self.config.max_retries + 1):
            try:
                logger.info(
                    "[LLM] 调用中 | provider=%s | attempt=%d/%d | prompt_len=%d",
                    self.config.provider, attempt, self.config.max_retries, len(prompt)
                )

                if self.config.provider == "dashscope":
                    result = self._call_dashscope(prompt, system_prompt, app_id)
                elif self.config.provider == "iflytek":
                    result = self._call_iflytek(prompt, system_prompt)
                else:
                    return LLMResponse(
                        success=False,
                        error_message=f"不支持的 provider: {self.config.provider}"
                    )

                if result.success:
                    logger.info(
                        "[LLM] 调用成功 | request_id=%s | response_len=%d",
                        result.request_id, len(result.content)
                    )
                    return result

                last_error = result.error_message
                logger.warning("[LLM] 调用失败 | attempt=%d | error=%s", attempt, last_error)

            except Exception as e:
                last_error = str(e)
                logger.error("[LLM] 异常 | attempt=%d | error=%s", attempt, last_error, exc_info=True)

            if attempt < self.config.max_retries:
                logger.info("[LLM] 等待 %.1fs 后重试...", retry_delay)
                time.sleep(retry_delay)
                retry_delay *= 2

        logger.error("[LLM] 已达最大重试次数 | 最终错误: %s", last_error)
        return LLMResponse(success=False, error_message=last_error)

    def call_with_messages(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        OpenAI 兼容模式调用（用于 knowledge_graph 等需要 messages 格式的场景）

        :param messages: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        :param temperature: 温度参数
        :param max_tokens: 最大token数
        :return: LLMResponse
        """
        if not messages:
            return LLMResponse(success=False, error_message="messages 不能为空")

        retry_delay = self.config.retry_delay
        last_error = ""

        for attempt in range(1, self.config.max_retries + 1):
            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url,
                )

                completion = client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=temperature or self.config.temperature,
                    max_tokens=max_tokens or self.config.max_tokens,
                )

                content = completion.choices[0].message.content.strip()
                return LLMResponse(
                    success=True,
                    content=content,
                    request_id=completion.id or "",
                    usage={
                        "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                        "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                    },
                    raw_response=completion,
                )

            except Exception as e:
                last_error = str(e)
                logger.error(
                    "[LLM] call_with_messages 异常 | attempt=%d | error=%s",
                    attempt, last_error, exc_info=True
                )
                if attempt < self.config.max_retries:
                    time.sleep(retry_delay)
                    retry_delay *= 2

        return LLMResponse(success=False, error_message=last_error)

    # ================================================================
    # 内部调用实现
    # ================================================================

    def _call_dashscope(
        self, prompt: str, system_prompt: Optional[str], app_id: Optional[str]
    ) -> LLMResponse:
        """调用通义千问 - 使用 OpenAI 兼容模式（更快）"""
        from openai import OpenAI

        full_prompt = prompt
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": full_prompt})

        client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
        )

        completion = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        content = completion.choices[0].message.content.strip()
        return LLMResponse(
            success=True,
            content=content,
            request_id=completion.id or "",
            usage={
                "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
            },
            raw_response=completion,
        )

    def _call_iflytek(self, prompt: str, system_prompt: Optional[str]) -> LLMResponse:
        """
        讯飞星火大模型调用（内联实现，直接从环境变量读取讯飞凭据）
        """
        import json
        import hmac
        import hashlib
        import base64
        import threading
        import time as _time
        import websocket as _ws
        from urllib.parse import urlencode, urlparse
        from datetime import datetime
        from wsgiref.handlers import format_date_time

        iflytek_app_id = os.getenv("IFLYTEK_APP_ID", "")
        iflytek_api_key = os.getenv("IFLYTEK_API_KEY", "")
        iflytek_api_secret = os.getenv("IFLYTEK_API_SECRET", "")
        model_version = os.getenv("IFLYTEK_MODEL_VERSION", "generalv3.5")

        domain_map = {
            "general": "wss://spark-api.xf-yun.com/v1.1/chat",
            "generalv2": "wss://spark-api.xf-yun.com/v2.1/chat",
            "generalv3": "wss://spark-api.xf-yun.com/v3.1/chat",
            "generalv3.5": "wss://spark-api.xf-yun.com/v3.5/chat",
            "generalv4.0": "wss://spark-api.xf-yun.com/v4.0/chat",
        }
        ws_url = domain_map.get(model_version, domain_map["generalv3.5"])

        if not iflytek_api_key or not iflytek_api_secret:
            return LLMResponse(success=False, error_message="IFLYTEK_API_KEY 或 IFLYTEK_API_SECRET 未配置")

        parsed = urlparse(ws_url)
        host = parsed.netloc
        path = parsed.path
        date = format_date_time(_time.mktime(datetime.now().timetuple()))

        signature_origin = "host: " + host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + path + " HTTP/1.1"

        signature_sha = hmac.new(
            iflytek_api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode("utf-8")

        authorization_origin = (
            f'api_key="{iflytek_api_key}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

        auth_url = f"{ws_url}?{urlencode({'authorization': authorization, 'date': date, 'host': host})}"

        text_list = []
        if system_prompt:
            text_list.append({"role": "system", "content": system_prompt})
        text_list.append({"role": "user", "content": prompt})

        request_frame = {
            "header": {"app_id": iflytek_app_id, "uid": "edu-platform-user"},
            "parameter": {"chat": {"domain": model_version, "temperature": 0.5, "max_tokens": 2048}},
            "payload": {"message": {"text": text_list}},
        }

        result_content = ""
        error_message = ""
        response_complete = threading.Event()
        send_done = threading.Event()

        logger.info("[iFlytek] 开始连接 | url=%s | model=%s", ws_url, model_version)

        def on_message(ws, message):
            nonlocal result_content, error_message
            try:
                data = json.loads(message)
                header = data.get("header", {})
                code = header.get("code", -1)
                if code != 0:
                    error_message = f"讯飞错误: code={code}, msg={header.get('message', '')}"
                    logger.error("[iFlytek] 收到错误响应: %s", error_message)
                    response_complete.set()
                    ws.close()
                    return
                choices = data.get("payload", {}).get("choices", {})
                for item in choices.get("text", []):
                    result_content += item.get("content", "")
                status_val = choices.get("status", -1)
                if status_val == 2:
                    logger.info("[iFlytek] 收到完整响应 | content_len=%d", len(result_content))
                    response_complete.set()
                    ws.close()
            except Exception as e:
                error_message = f"响应解析异常: {str(e)}"
                logger.error("[iFlytek] %s", error_message, exc_info=True)
                response_complete.set()
                ws.close()

        def on_error(ws, error):
            nonlocal error_message
            error_message = f"WebSocket错误: {str(error)}"
            logger.error("[iFlytek] %s", error_message)
            response_complete.set()

        def on_open(ws):
            logger.info("[iFlytek] WebSocket连接已建立，开始发送请求")
            try:
                ws.send(json.dumps(request_frame))
                send_done.set()
                logger.info("[iFlytek] 请求帧已发送")
            except Exception as e:
                error_message = f"发送请求失败: {str(e)}"
                logger.error("[iFlytek] %s", error_message)
                send_done.set()
                response_complete.set()
                ws.close()

        def on_close(ws, close_status_code, close_msg):
            logger.info("[iFlytek] WebSocket连接关闭 | code=%s | msg=%s", close_status_code, close_msg)
            response_complete.set()

        _ws.enableTrace(False)
        ws_app = _ws.WebSocketApp(
            auth_url,
            on_message=on_message,
            on_error=on_error,
            on_open=on_open,
            on_close=on_close,
        )

        ws_thread = threading.Thread(target=ws_app.run_forever, daemon=True)
        ws_thread.start()

        completed = response_complete.wait(timeout=self.config.timeout)
        if not completed:
            logger.warning("[iFlytek] 请求超时 (%ds)，关闭连接", self.config.timeout)
            ws_app.close()
            return LLMResponse(success=False, error_message=f"讯飞请求超时 ({self.config.timeout}s)")

        if error_message:
            return LLMResponse(success=False, error_message=error_message)
        if not result_content:
            return LLMResponse(success=False, error_message="讯飞返回内容为空")

        return LLMResponse(success=True, content=result_content.strip())
