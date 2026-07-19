"""
讯飞星火大模型适配器

讯飞星火 API 使用 WebSocket 协议进行流式通信，
鉴权方式为 HMAC-SHA256 签名。

已实现：
- 鉴权 URL 生成（HMAC-SHA256 + Base64）
- WebSocket 连接管理
- 流式响应拼接
- 错误码映射
- 与 LLMAdapter 统一的调用接口

参考文档: https://www.xfyun.cn/doc/spark/Web.html
"""

import os
import json
import time
import hmac
import hashlib
import base64
import logging
import threading
from urllib.parse import urlencode, urlparse
from datetime import datetime
from typing import Optional
from wsgiref.handlers import format_date_time

import websocket

from adapters.llm_adapter import LLMAdapter, LLMConfig, LLMResponse

logger = logging.getLogger(__name__)

IFLYTEK_ERROR_CODES = {
    0: "成功",
    10001: "参数错误",
    10002: "鉴权失败",
    10003: "配额不足",
    10004: "appId与接口不匹配",
    10005: "会话错误",
    10007: "引擎错误",
    10008: "模型服务不可用",
    10009: "会话超时",
    10010: "系统异常",
    10011: "请求频率超限",
    10012: "输入文本过长",
    10013: "音频数据错误",
    10014: "内容审核未通过",
}

DOMAIN_MAP = {
    "general": "wss://spark-api.xf-yun.com/v1.1/chat",
    "generalv2": "wss://spark-api.xf-yun.com/v2.1/chat",
    "generalv3": "wss://spark-api.xf-yun.com/v3.1/chat",
    "generalv3.5": "wss://spark-api.xf-yun.com/v3.5/chat",
    "generalv4.0": "wss://spark-api.xf-yun.com/v4.0/chat",
}


class IflytekConfig:
    """讯飞星火配置"""

    def __init__(self):
        self.app_id = os.getenv("IFLYTEK_APP_ID", "")
        self.api_key = os.getenv("IFLYTEK_API_KEY", "")
        self.api_secret = os.getenv("IFLYTEK_API_SECRET", "")
        self.model_version = os.getenv("IFLYTEK_MODEL_VERSION", "generalv3.5")
        self.ws_url = DOMAIN_MAP.get(self.model_version, DOMAIN_MAP["generalv3.5"])


class IflytekAdapter(LLMAdapter):
    """
    讯飞星火大模型适配器

    继承 LLMAdapter，实现 _call_iflytek 方法，
    通过 WebSocket 协议与讯飞星火服务通信。

    使用方式:
        from adapters.llm_adapter import LLMConfig
        config = LLMConfig(provider="iflytek", api_key="your_key")
        adapter = IflytekAdapter(config)
        response = adapter.call("你好")
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config)
        self.iflytek_config = IflytekConfig()
        self._validate_iflytek_config()

    def _validate_iflytek_config(self):
        """校验讯飞配置"""
        if not self.iflytek_config.app_id:
            logger.warning("[iFlytek] IFLYTEK_APP_ID 未配置")
        if not self.iflytek_config.api_key:
            logger.warning("[iFlytek] IFLYTEK_API_KEY 未配置")
        if not self.iflytek_config.api_secret:
            logger.warning("[iFlytek] IFLYTEK_API_SECRET 未配置")

    def _call_iflytek(self, prompt: str, system_prompt: Optional[str]) -> LLMResponse:
        """
        讯飞星火大模型调用（完整实现）

        流程：
        1. 生成鉴权 URL
        2. 建立 WebSocket 连接
        3. 发送请求帧
        4. 接收流式响应并拼接
        5. 返回统一 LLMResponse
        """
        logger.info("[iFlytek] 开始调用 | model=%s | prompt_len=%d",
                     self.iflytek_config.model_version, len(prompt))

        try:
            auth_url = self._generate_auth_url()
        except Exception as e:
            logger.error("[iFlytek] 鉴权URL生成失败: %s", e)
            return LLMResponse(success=False, error_message=f"鉴权失败: {str(e)}")

        request_frame = self._build_request_frame(prompt, system_prompt)

        result_content = ""
        error_message = ""
        response_complete = threading.Event()

        def on_message(ws, message):
            nonlocal result_content, error_message
            try:
                parsed = self._parse_response(message)
                if parsed["code"] != 0:
                    error_message = f"讯飞返回错误: code={parsed['code']}, msg={IFLYTEK_ERROR_CODES.get(parsed['code'], '未知错误')}"
                    response_complete.set()
                    ws.close()
                    return

                result_content += parsed["content"]

                if parsed["status"] == 2:
                    logger.info("[iFlytek] 响应完成 | response_len=%d", len(result_content))
                    response_complete.set()
                    ws.close()

            except Exception as e:
                error_message = f"响应解析异常: {str(e)}"
                logger.error("[iFlytek] %s", error_message)
                response_complete.set()
                ws.close()

        def on_error(ws, error):
            nonlocal error_message
            error_message = f"WebSocket错误: {str(error)}"
            logger.error("[iFlytek] %s", error_message)
            response_complete.set()

        def on_open(ws):
            def run():
                ws.send(json.dumps(request_frame))
            threading.Thread(target=run, daemon=True).start()

        def on_close(ws, close_status_code, close_msg):
            logger.info("[iFlytek] WebSocket连接关闭 | status=%s | msg=%s", close_status_code, close_msg)
            response_complete.set()

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            auth_url,
            on_message=on_message,
            on_error=on_error,
            on_open=on_open,
            on_close=on_close,
        )

        logger.info("[iFlytek] 开始建立WebSocket连接...")
        ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
        ws_thread.start()

        timeout = self.config.timeout
        logger.info("[iFlytek] 等待响应，超时时间: %ds", timeout)
        completed = response_complete.wait(timeout=timeout)

        if not completed:
            ws.close()
            logger.error("[iFlytek] 请求超时 (%ds) | 可能原因：网络问题、凭证错误、或服务不可用", timeout)
            return LLMResponse(success=False, error_message=f"讯飞请求超时 ({timeout}s)")

        if error_message:
            return LLMResponse(success=False, error_message=error_message)

        if not result_content:
            return LLMResponse(success=False, error_message="讯飞返回内容为空")

        return LLMResponse(
            success=True,
            content=result_content.strip(),
            request_id="",
            usage={},
        )

    def _generate_auth_url(self) -> str:
        """
        生成讯飞鉴权 URL

        鉴权流程：
        1. 拼接 host, path, date 为 signature_origin
        2. 使用 HMAC-SHA256 + api_secret 生成签名
        3. 拼接 authorization
        4. Base64 编码
        5. 拼接到 ws URL 参数中
        """
        api_secret = self.iflytek_config.api_secret
        api_key = self.iflytek_config.api_key

        if not api_secret or not api_key:
            raise ValueError("IFLYTEK_API_SECRET 或 IFLYTEK_API_KEY 未配置")

        parsed_url = urlparse(self.iflytek_config.ws_url)
        host = parsed_url.netloc
        path = parsed_url.path

        now = datetime.now()
        date = format_date_time(time.mktime(now.timetuple()))

        signature_origin = "host: " + host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + path + " HTTP/1.1"

        signature_sha = hmac.new(
            api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        signature_sha = base64.b64encode(signature_sha).decode("utf-8")

        authorization_origin = (
            f'api_key="{api_key}", '
            f'algorithm="hmac-sha256", '
            f'headers="host date request-line", '
            f'signature="{signature_sha}"'
        )

        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

        params = {
            "authorization": authorization,
            "date": date,
            "host": host,
        }

        auth_url = f"{self.iflytek_config.ws_url}?{urlencode(params)}"
        logger.info("[iFlytek] 鉴权URL已生成 | model=%s", self.iflytek_config.model_version)
        return auth_url

    def _build_request_frame(self, prompt: str, system_prompt: Optional[str]) -> dict:
        """
        构建讯飞请求帧

        格式：
        {
            "header": {"app_id": "...", "uid": "..."},
            "parameter": {"chat": {"domain": "...", "temperature": 0.5, ...}},
            "payload": {"message": {"text": [...]}}
        }
        """
        text_list = []

        if system_prompt:
            text_list.append({
                "role": "system",
                "content": system_prompt
            })

        text_list.append({
            "role": "user",
            "content": prompt
        })

        domain = self.iflytek_config.model_version

        frame = {
            "header": {
                "app_id": self.iflytek_config.app_id,
                "uid": "edu-platform-user",
            },
            "parameter": {
                "chat": {
                    "domain": domain,
                    "temperature": self.config.temperature if hasattr(self.config, 'temperature') else 0.5,
                    "max_tokens": self.config.max_tokens if hasattr(self.config, 'max_tokens') else 2048,
                }
            },
            "payload": {
                "message": {
                    "text": text_list
                }
            },
        }

        logger.info("[iFlytek] 请求帧已构建 | domain=%s | messages=%d", domain, len(text_list))
        return frame

    def _parse_response(self, ws_message: str) -> dict:
        """
        解析讯飞 WebSocket 响应帧

        响应格式：
        {
            "header": {"code": 0, "status": 0/1/2, "sid": "..."},
            "payload": {"choices": {"status": 0/1/2, "seq": 0, "text": [{"content": "..."}]}}
        }
        """
        data = json.loads(ws_message)

        header = data.get("header", {})
        code = header.get("code", -1)
        status = header.get("status", -1)

        if code != 0:
            logger.error("[iFlytek] 响应错误 | code=%d | sid=%s", code, header.get("sid", ""))
            return {"code": code, "content": "", "status": status}

        choices = data.get("payload", {}).get("choices", {})
        response_status = choices.get("status", status)
        text_list = choices.get("text", [])

        content = ""
        for item in text_list:
            content += item.get("content", "")

        return {
            "code": code,
            "content": content,
            "status": response_status,
        }
