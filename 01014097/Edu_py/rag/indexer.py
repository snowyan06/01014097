"""
RAG 索引器骨架

功能：将原始文档进行分块、向量化，建立索引
TODO: 实现文档分块策略 + Embedding 生成 + 索引持久化

依赖:
- 文档解析库（PyPDF2、python-docx）
- Embedding 模型（DashScope / 本地模型）
- 向量数据库（FAISS / ChromaDB）
"""

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class Indexer:
    """知识库索引器"""

    def __init__(self, knowledge_base_path: str = "rag/knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        logger.info("[Indexer] 初始化 | path=%s", knowledge_base_path)

    def index_documents(self, file_paths: List[str]) -> bool:
        """
        对文档建立索引（待实现）

        :param file_paths: 文档文件路径列表
        :return: 是否成功
        """
        logger.warning("[Indexer] 索引功能尚未实现")
        return False

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        文本分块（待实现）

        :param text: 原始文本
        :param chunk_size: 每块最大字符数
        :param overlap: 块间重叠字符数
        :return: 分块后的文本列表
        """
        raise NotImplementedError("文本分块功能尚未实现")
