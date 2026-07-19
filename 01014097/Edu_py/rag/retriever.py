"""
RAG 检索器骨架

功能：根据用户查询，从知识库中检索最相关的文档片段
TODO: 实现向量检索 + 关键词混合检索

依赖:
- 向量数据库（如 FAISS / ChromaDB）
- Embedding 模型
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class Retriever:
    """知识库检索器"""

    def __init__(self, knowledge_base_path: str = "rag/knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        logger.info("[Retriever] 初始化 | path=%s", knowledge_base_path)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        检索知识库（待实现）

        :param query: 查询文本
        :param top_k: 返回最相关的 top_k 条结果
        :return: [{"content": "...", "source": "...", "score": 0.95}, ...]
        """
        logger.warning("[Retriever] 检索功能尚未实现")
        return []
