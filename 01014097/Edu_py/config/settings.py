"""
统一配置管理
消除各文件重复的环境变量读取和硬编码密钥
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """全局配置，集中管理所有环境变量"""

    # ====================
    # 数据库配置
    # ====================
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "123456")
    DB_NAME: str = os.getenv("DB_NAME", "mydb")

    # ====================
    # 通义千问 DashScope 配置
    # ====================
    API_KEY: str = os.getenv("OTHER_API_KEY", "")
    APP_ID: str = os.getenv("APP_ID", "")
    STUDENT_APP_ID: str = os.getenv("STUDENT_APP_ID", "")
    TEACHER_APP_ID: str = os.getenv("TEACHER_APP_ID", "")
    DASH_SCOPE_API_KEY: str = os.getenv("DASH_SCOPE_API_KEY", "")

    # ====================
    # 通用 LLM 调用配置
    # ====================
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "dashscope")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen-turbo")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))

    # ====================
    # 讯飞星火大模型配置（预留）
    # ====================
    IFLYTEK_APP_ID: str = os.getenv("IFLYTEK_APP_ID", "")
    IFLYTEK_API_KEY: str = os.getenv("IFLYTEK_API_KEY", "")
    IFLYTEK_API_SECRET: str = os.getenv("IFLYTEK_API_SECRET", "")

    # ====================
    # 讯飞语音服务配置（预留）
    # ====================
    IFLYTEK_STT_APP_ID: str = os.getenv("IFLYTEK_STT_APP_ID", "")
    IFLYTEK_STT_API_KEY: str = os.getenv("IFLYTEK_STT_API_KEY", "")
    IFLYTEK_TTS_APP_ID: str = os.getenv("IFLYTEK_TTS_APP_ID", "")
    IFLYTEK_TTS_API_KEY: str = os.getenv("IFLYTEK_TTS_API_KEY", "")

    # ====================
    # 文件存储配置
    # ====================
    FILE_STORAGE_PATH: str = os.getenv("FILE_STORAGE_PATH", "./storage/files")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")

    # ====================
    # 数字人 / 前端配置
    # ====================
    AVATAR_PORT: int = int(os.getenv("AVATAR_PORT", "8010"))
    TTS_SERVER: str = os.getenv("TTS_SERVER", "http://127.0.0.1:9880")

    @classmethod
    def get_db_config(cls) -> dict:
        """获取数据库连接配置字典"""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME,
            "charset": "utf8mb4",
        }


settings = Settings()
