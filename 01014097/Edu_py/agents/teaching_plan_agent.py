"""
教学计划生成 Agent
迁移自 chat.py，负责：
- 根据课程大纲生成教学计划文本
- 生成 Mermaid 图表代码并渲染为 PNG
"""

import os
import time
import logging
import subprocess
import tempfile
from typing import Dict, Any

from agents.base_agent import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class TeachingPlanAgent(BaseAgent):
    """教学计划生成 Agent"""

    agent_name: str = "teaching_plan"
    agent_description: str = "根据课程大纲生成教学计划及 Mermaid 可视化图表"

    def __init__(self, adapter=None, app_id=None):
        super().__init__(adapter, app_id or settings.APP_ID)

    # ================================================================
    # Prompt 构建
    # ================================================================

    @staticmethod
    def _build_prompt(course_outline: dict) -> str:
        return f"""
你是一位资深教师，根据以下课程大纲，设计一份完整的教学内容，包括：
1. 知识讲解（分知识点说明）
2. 实训练习与指导（含示例和练习题）
3. 时间分配建议（总时长为 4 小时）

请严格按照以下格式输出，不要使用 Markdown 格式，只输出纯文本：

【课程名称】{course_outline.get("name", "未命名课程")}
【总时长】4小时

【知识讲解】
1. {{知识点1}}（约{{分钟数}}分钟）
   - {{讲解内容}}
2. {{知识点2}}（约{{分钟数}}分钟）
   - {{讲解内容}}

【实训练习】
1. {{练习题1}}
   - 指导建议：{{指导说明}}
2. {{练习题2}}
   - 指导建议：{{指导说明}}

【时间分布】
- 知识讲解：XX分钟
- 实训练习：XX分钟
- 总结回顾：XX分钟

现在请你根据以下课程大纲内容来填充上面的内容：

---
{course_outline.get("content", "")}
""".strip()

    @staticmethod
    def _build_mermaid_prompt(content: str) -> str:
        return f"""
你是一个擅长可视化表达的教育专家。请根据以下教学计划内容，生成两个 Mermaid 图表代码：

1. 一个 **思维导图（mindmap）**，展示课程的整体结构。
2. 一个 **流程图（flowchart）**，表示教学过程的时间顺序。

要求如下：

=== MINDMAP ===
- 使用 Mermaid 的 `mindmap` 图类型
- 中心节点格式：`root((教学计划))`
- 子节点直接缩进表示层级
- 示例格式：
  mindmap
    root((教学计划))
      知识讲解
        知识点1
        知识点2
      实训练习
        练习1
        练习2
      时间分布
        知识讲解
        实训练习
        总结回顾
- 不要使用 ``` 包裹，只输出代码

=== FLOWCHART ===
- 使用 `flowchart TB`（从上到下）
- 表示教学流程顺序：开始 → 知识讲解 → 实训练习 → 总结回顾 → 结束
- 可加入关键知识点或练习作为子步骤
- 示例：
  flowchart TB
    A[开始] --> B[知识讲解]
    B --> B1[变量与数据类型]
    B --> B2[条件语句]
    B --> B3[循环结构]
    B --> B4[函数]
    B --> C[实训练习]
    C --> C1[练习1：判断闰年]
    C --> C2[练习2：求和]
    C --> D[总结回顾]
    D --> E[课程结束]

请严格按照以下格式输出，不要添加额外说明：

=== MINDMAP ===
mindmap
  root((教学计划))
  ...

=== FLOWCHART ===
flowchart TB
  ...

教学内容如下：
{content}
""".strip()

    # ================================================================
    # Mermaid 工具方法
    # ================================================================

    @staticmethod
    def _check_mmdc_installation():
        """检查是否已安装 mermaid-cli"""
        possible_commands = [
            'mmdc', 'mmdc.cmd', 'npx mmdc',
            r'D:\Program Files\nodejs\node_global\mmdc.ps1',
            ['powershell', '-Command', 'mmdc']
        ]

        for cmd in possible_commands:
            try:
                if isinstance(cmd, str):
                    cmd_list = cmd.split() + ['--version']
                else:
                    cmd_list = cmd + ['--version']

                subprocess.run(cmd_list, capture_output=True, text=True, check=True, timeout=10)

                if isinstance(cmd, str):
                    return True, cmd.split()
                else:
                    return True, cmd
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue

        try:
            npm_bin_result = subprocess.run(
                ['npm', 'bin', '-g'], capture_output=True, text=True, check=True, timeout=10
            )
            npm_bin_path = npm_bin_result.stdout.strip()

            for filename in ['mmdc.cmd', 'mmdc', 'mmdc.ps1']:
                mmdc_full_path = os.path.join(npm_bin_path, filename)
                if os.path.exists(mmdc_full_path):
                    try:
                        if filename.endswith('.ps1'):
                            subprocess.run(
                                ['powershell', '-Command', f'& "{mmdc_full_path}" --version'],
                                capture_output=True, text=True, check=True, timeout=10
                            )
                            return True, ['powershell', '-Command', f'& "{mmdc_full_path}"']
                        else:
                            subprocess.run(
                                [mmdc_full_path, '--version'],
                                capture_output=True, text=True, check=True, timeout=10
                            )
                            return True, [mmdc_full_path]
                    except:
                        continue
        except:
            pass

        return False, None

    @staticmethod
    def _generate_mermaid_png(mermaid_code: str, output_path: str, mmdc_cmd) -> tuple:
        """将 Mermaid 代码转换为 PNG 图片"""
        temp_mmd_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(mermaid_code)
                temp_mmd_path = temp_file.name

            if isinstance(mmdc_cmd, list) and len(mmdc_cmd) > 1 and 'powershell' in mmdc_cmd[0].lower():
                base_cmd = mmdc_cmd[:-1]
                ps_script = f'& {mmdc_cmd[-1]} -i "{temp_mmd_path}" -o "{output_path}" -b white'
                cmd = base_cmd + [ps_script]
            else:
                cmd = mmdc_cmd + ['-i', temp_mmd_path, '-o', output_path, '-b', 'white']

            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)

            if os.path.exists(output_path):
                return True, f"图片生成成功: {output_path}"
            return False, "图片文件未生成"

        except subprocess.CalledProcessError as e:
            return False, f"mmdc 命令执行失败: {e.stderr if e.stderr else e.stdout}"
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, f"生成图片时发生错误: {str(e)}"
        finally:
            if temp_mmd_path and os.path.exists(temp_mmd_path):
                os.unlink(temp_mmd_path)

    # ================================================================
    # 主处理方法
    # ================================================================

    def process(self, **kwargs) -> Dict[str, Any]:
        """
        生成教学计划

        :param course_outline: {"name": str, "content": str}
        """
        course_outline = kwargs.get("course_outline")
        if not course_outline:
            return self._build_error_response("缺少 course_outline 参数")

        mmdc_available, mmdc_cmd = self._check_mmdc_installation()
        if not mmdc_available:
            return self._build_error_response(
                "未检测到 @mermaid-js/mermaid-cli。请先安装：npm install -g @mermaid-js/mermaid-cli"
            )

        try:
            prompt = self._build_prompt(course_outline)
            response = self.call_llm(prompt)
            if not response.success:
                return self._build_error_response(f"教学计划生成失败: {response.error_message}")

            content = response.content

            base_dir = settings.FILE_STORAGE_PATH
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename_txt = f"teaching_plan_{timestamp}.txt"
            file_path_txt = os.path.join(base_dir, filename_txt)
            os.makedirs(base_dir, exist_ok=True)

            with open(file_path_txt, "w", encoding="utf-8") as f:
                f.write(content)

            file_size_txt = os.path.getsize(file_path_txt)

            mermaid_prompt = self._build_mermaid_prompt(content)
            mermaid_response = self.call_llm(mermaid_prompt)

            mindmap_png_path = None
            flowchart_png_path = None
            mindmap_success = False
            flowchart_success = False
            mindmap_message = ""
            flowchart_message = ""

            if not mermaid_response.success:
                mindmap_message = "Mermaid 代码生成失败"
                flowchart_message = "Mermaid 代码生成失败"
            else:
                mermaid_output = mermaid_response.content
                parts = {}
                current_key = None

                for line in mermaid_output.splitlines():
                    if line.strip() == "=== MINDMAP ===":
                        current_key = "mindmap"
                        parts[current_key] = []
                    elif line.strip() == "=== FLOWCHART ===":
                        current_key = "flowchart"
                        parts[current_key] = []
                    elif current_key:
                        parts[current_key].append(line)

                mermaid_mindmap = "\n".join(parts.get("mindmap", [])).strip()
                mermaid_flowchart = "\n".join(parts.get("flowchart", [])).strip()

                mermaid_mindmap = mermaid_mindmap.replace("```mermaid", "").replace("```", "").strip()
                mermaid_flowchart = mermaid_flowchart.replace("```mermaid", "").replace("```", "").strip()

                if mermaid_mindmap and not mermaid_mindmap.startswith("mindmap"):
                    mermaid_mindmap = "mindmap\n" + mermaid_mindmap
                if mermaid_flowchart and not mermaid_flowchart.startswith("flowchart"):
                    mermaid_flowchart = "flowchart TB\n" + mermaid_flowchart

                if mermaid_mindmap:
                    mindmap_png_path = os.path.join(base_dir, f"mindmap_{timestamp}.png")
                    mindmap_success, mindmap_message = self._generate_mermaid_png(
                        mermaid_mindmap, mindmap_png_path, mmdc_cmd
                    )
                    if not mindmap_success:
                        mindmap_png_path = None

                if mermaid_flowchart:
                    flowchart_png_path = os.path.join(base_dir, f"flowchart_{timestamp}.png")
                    flowchart_success, flowchart_message = self._generate_mermaid_png(
                        mermaid_flowchart, flowchart_png_path, mmdc_cmd
                    )
                    if not flowchart_success:
                        flowchart_png_path = None

            return self._build_success_response(
                data={
                    "content": content,
                    "images": {
                        "mindmap": {
                            "success": mindmap_success,
                            "path": mindmap_png_path,
                            "message": mindmap_message,
                            "size_bytes": os.path.getsize(mindmap_png_path) if mindmap_png_path and os.path.exists(mindmap_png_path) else 0
                        },
                        "flowchart": {
                            "success": flowchart_success,
                            "path": flowchart_png_path,
                            "message": flowchart_message,
                            "size_bytes": os.path.getsize(flowchart_png_path) if flowchart_png_path and os.path.exists(flowchart_png_path) else 0
                        }
                    }
                },
                message="教学计划生成成功"
            )

        except Exception as e:
            logger.error("[Agent:teaching_plan] 异常: %s", e, exc_info=True)
            return self._build_error_response(str(e))
