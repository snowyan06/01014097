"""
AI 输出过滤与专业化教育话术处理

功能：
- 过滤 AI 生成内容中的机器生硬表述
- 统一转换为专业化教育话术
- 移除不当内容（如过度口语化、不严谨表述）
- 确保输出适配前端展示

使用方式:
    from services.output_filter import filter_output
    clean_text = filter_output(raw_ai_text)
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ================================================================
# 过滤规则配置
# ================================================================

# 机器生硬表述 -> 专业化教育话术 替换映射
REPLACEMENT_RULES = {
    r"作为AI(?:语言)?(?:模型|助手)，我(?:无法|不能|不具备)": "根据教学内容分析，",
    r"抱歉，我(?:无法|不能)": "很抱歉，目前",
    r"根据我的(?:了解|知识|分析)": "根据课程内容",
    r"请注意，这(?:只是|仅仅)是(?:我的|AI的)(?:理解|分析|建议)": "需要特别关注的是",
    r"希望这(?:个答案|对你|能帮)能(?:够)?帮(?:助)?到你": "掌握以上要点，有助于后续学习",
    r"让我(?:来)?(?:为你|帮你)?(?:解释|解答|分析)": "下面进行详细解析",
    r"首先.*其次.*最后": "① 要点梳理 ② 重点突破 ③ 巩固提升",
    r"综上所述": "归纳总结",
    r"需要注意的是": "易错提醒",
    r"希望以上.*对你.*帮助": "建议结合课堂练习巩固理解",
}

# 需要移除/替换的前缀标记
NOISE_PREFIXES = [
    r"^好的[，,]?\s*",
    r"^当然[可以]?\s*",
    r"^没问题[，,]?\s*",
    r"^让我(?:来)?(?:为你|帮你)?\s*",
    r"^以下是.*(?:答案|解析|回答)[：:]\s*",
]

# 需要过滤的危险内容关键词
BLOCKED_KEYWORDS = [
    "我不确定", "我不清楚", "这超出了我的能力",
    "作为语言模型", "作为一个AI",
]


def filter_output(raw_text: str, agent_name: str = "unknown") -> str:
    """
    AI输出过滤主入口

    :param raw_text: AI原始输出文本
    :param agent_name: 调用方Agent名称（用于日志追踪）
    :return: 过滤后的专业化文本
    """
    if not raw_text or not raw_text.strip():
        logger.warning("[Filter] 收到空文本，Agent=%s", agent_name)
        return ""

    filtered = raw_text.strip()

    # 1. 移除噪音前缀
    for pattern in NOISE_PREFIXES:
        filtered = re.sub(pattern, "", filtered, flags=re.IGNORECASE)

    # 2. 应用话术替换规则
    for pattern, replacement in REPLACEMENT_RULES.items():
        filtered = re.sub(pattern, replacement, filtered, flags=re.IGNORECASE)

    # 3. 检查危险内容
    for keyword in BLOCKED_KEYWORDS:
        if keyword in filtered:
            logger.warning(
                "[Filter] 检测到不当表述 | keyword=%s | agent=%s",
                keyword, agent_name
            )
            filtered = filtered.replace(keyword, "")

    # 4. 清理多余空行和空格
    filtered = re.sub(r"\n{3,}", "\n\n", filtered)
    filtered = re.sub(r" {2,}", " ", filtered)

    if filtered != raw_text.strip():
        logger.info("[Filter] 文本已过滤 | agent=%s | 原长度=%d | 过滤后长度=%d",
                     agent_name, len(raw_text), len(filtered))

    return filtered.strip()


def validate_education_content(text: str) -> dict:
    """
    校验文本是否符合教育场景规范

    :param text: 待校验文本
    :return: {"valid": bool, "warnings": [...]}
    """
    warnings = []

    if not text or not text.strip():
        return {"valid": False, "warnings": ["内容为空"]}

    if len(text) < 10:
        warnings.append("内容过短，可能不够完整")

    for keyword in BLOCKED_KEYWORDS:
        if keyword in text:
            warnings.append(f"包含不当表述: '{keyword}'")

    return {
        "valid": len(warnings) == 0,
        "warnings": warnings,
    }
