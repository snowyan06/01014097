from http import HTTPStatus
from dashscope import Application
import os
import time
import subprocess
import tempfile


def build_prompt(course_outline):
    prompt = f"""
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
"""
    return prompt.strip()


def build_mermaid_prompt(content):
    prompt = f"""
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
"""
    return prompt.strip()


def check_mmdc_installation():
    """检查是否已安装 mermaid-cli"""
    # 尝试多种可能的命令路径
    possible_commands = [
        'mmdc',
        'mmdc.cmd',
        'npx mmdc',
        # 根据你的系统路径，添加 PowerShell 脚本路径
        r'D:\Program Files\nodejs\node_global\mmdc.ps1',
        # 也可以通过 PowerShell 调用
        ['powershell', '-Command', 'mmdc']
    ]

    for cmd in possible_commands:
        try:
            if isinstance(cmd, str):
                cmd_list = cmd.split() + ['--version']
            else:
                cmd_list = cmd + ['--version']

            result = subprocess.run(cmd_list,
                                    capture_output=True, text=True, check=True,
                                    timeout=10)


            if isinstance(cmd, str):
                return True, cmd.split()
            else:
                return True, cmd
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # 如果都找不到，尝试通过 npm 查找
    try:
        npm_bin_result = subprocess.run(['npm', 'bin', '-g'],
                                        capture_output=True, text=True, check=True,
                                        timeout=10)
        npm_bin_path = npm_bin_result.stdout.strip()

        # 尝试不同的可能文件名
        possible_files = ['mmdc.cmd', 'mmdc', 'mmdc.ps1']
        for filename in possible_files:
            mmdc_full_path = os.path.join(npm_bin_path, filename)
            if os.path.exists(mmdc_full_path):
                # 测试完整路径
                try:
                    if filename.endswith('.ps1'):
                        # PowerShell 脚本需要特殊处理
                        result = subprocess.run(['powershell', '-Command', f'& "{mmdc_full_path}" --version'],
                                                capture_output=True, text=True, check=True,
                                                timeout=10)

                        return True, ['powershell', '-Command', f'& "{mmdc_full_path}"']
                    else:
                        result = subprocess.run([mmdc_full_path, '--version'],
                                                capture_output=True, text=True, check=True,
                                                timeout=10)

                        return True, [mmdc_full_path]
                except:
                    continue
    except:
        pass

    return False, None


def generate_mermaid_png(mermaid_code, output_path, mmdc_cmd):
    """将 Mermaid 代码转换为 PNG 图片"""
    try:
        # 创建临时 mmd 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd',
                                         delete=False, encoding='utf-8') as temp_file:
            temp_file.write(mermaid_code)
            temp_mmd_path = temp_file.name

        # 构建命令
        if isinstance(mmdc_cmd, list) and len(mmdc_cmd) > 1 and 'powershell' in mmdc_cmd[0].lower():
            # 处理 PowerShell 命令
            base_cmd = mmdc_cmd[:-1]  # 移除最后一个元素（可能是不完整的命令）
            ps_script = f'& {mmdc_cmd[-1]} -i "{temp_mmd_path}" -o "{output_path}" -b white'
            cmd = base_cmd + [ps_script]
        else:
            # 普通命令
            cmd = mmdc_cmd + ['-i', temp_mmd_path, '-o', output_path, '-b', 'white']



        result = subprocess.run(cmd, capture_output=True, text=True,
                                check=True, timeout=60)  # 增加超时时间

        # 清理临时文件
        os.unlink(temp_mmd_path)

        if os.path.exists(output_path):
            return True, f"图片生成成功: {output_path}"
        else:
            return False, "图片文件未生成"

    except subprocess.CalledProcessError as e:
        # 清理临时文件
        if 'temp_mmd_path' in locals() and os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)
        error_msg = f"mmdc 命令执行失败: {e.stderr if e.stderr else e.stdout}"
        return False, error_msg
    except subprocess.TimeoutExpired:
        # 清理临时文件
        if 'temp_mmd_path' in locals() and os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)
        return False, "命令执行超时"
    except Exception as e:
        # 清理临时文件
        if 'temp_mmd_path' in locals() and os.path.exists(temp_mmd_path):
            os.unlink(temp_mmd_path)
        return False, f"生成图片时发生错误: {str(e)}"


def generate_teaching_plan(course_outline, api_key, app_id):
    # 首先检查 mmdc 是否已安装
    mmdc_available, mmdc_cmd = check_mmdc_installation()
    if not mmdc_available:
        return {
            "success": False,
            "error": "未检测到 @mermaid-js/mermaid-cli。请先安装：npm install -g @mermaid-js/mermaid-cli\n或者检查环境变量 PATH 是否包含 npm 全局模块路径"
        }

    # 构建初始提示词并生成教学计划
    prompt = build_prompt(course_outline)

    try:
        # 第一步：生成教学计划文本
        response = Application.call(
            api_key=api_key,
            app_id=app_id,
            prompt=prompt
        )

        if response.status_code != HTTPStatus.OK:
            error_data = {
                "success": False,
                "code": response.status_code,
                "message": response.message,
                "request_id": getattr(response, 'request_id', None)
            }
            return error_data

        content = response.output.text

        # 第二步：保存原始教学计划文本
        base_dir = r"E:\xmugli\Edu_platform\storage\files"
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename_txt = f"teaching_plan_{timestamp}.txt"
        file_path_txt = os.path.join(base_dir, filename_txt)

        os.makedirs(base_dir, exist_ok=True)

        with open(file_path_txt, "w", encoding="utf-8") as f:
            f.write(content)

        file_size_txt = os.path.getsize(file_path_txt)

        # 第三步：调用模型生成 Mermaid 图表代码
        mermaid_prompt = build_mermaid_prompt(content)
        mermaid_response = Application.call(
            api_key=api_key,
            app_id=app_id,
            prompt=mermaid_prompt
        )

        mindmap_png_path = None
        flowchart_png_path = None
        mindmap_success = False
        flowchart_success = False
        mindmap_message = ""
        flowchart_message = ""

        if mermaid_response.status_code != HTTPStatus.OK:
            mindmap_message = "Mermaid 代码生成失败"
            flowchart_message = "Mermaid 代码生成失败"
        else:
            mermaid_output = mermaid_response.output.text

            # 尝试按标记分割
            parts = {}
            current_key = None
            lines = mermaid_output.splitlines()

            for line in lines:
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

            # 清理可能的代码块标记
            mermaid_mindmap = mermaid_mindmap.replace("```mermaid", "").replace("```", "").strip()
            mermaid_flowchart = mermaid_flowchart.replace("```mermaid", "").replace("```", "").strip()

            # 验证是否以正确格式开头，否则补充
            if mermaid_mindmap and not mermaid_mindmap.startswith("mindmap"):
                mermaid_mindmap = "mindmap\n" + mermaid_mindmap

            if mermaid_flowchart and not mermaid_flowchart.startswith("flowchart"):
                mermaid_flowchart = "flowchart TB\n" + mermaid_flowchart

            # 生成思维导图 PNG
            if mermaid_mindmap:
                mindmap_png_path = os.path.join(base_dir, f"mindmap_{timestamp}.png")
                mindmap_success, mindmap_message = generate_mermaid_png(
                    mermaid_mindmap, mindmap_png_path, mmdc_cmd
                )
                if not mindmap_success:
                    mindmap_png_path = None

            # 生成流程图 PNG
            if mermaid_flowchart:
                flowchart_png_path = os.path.join(base_dir, f"flowchart_{timestamp}.png")
                flowchart_success, flowchart_message = generate_mermaid_png(
                    mermaid_flowchart, flowchart_png_path, mmdc_cmd
                )
                if not flowchart_success:
                    flowchart_png_path = None

        # 返回结果
        return {
            "success": True,
            "data": {
                "content": content,
                "images": {
                    "mindmap": {
                        "success": mindmap_success,
                        "path": mindmap_png_path,
                        "message": mindmap_message,
                        "size_bytes": os.path.getsize(mindmap_png_path) if mindmap_png_path and os.path.exists(
                            mindmap_png_path) else 0
                    },
                    "flowchart": {
                        "success": flowchart_success,
                        "path": flowchart_png_path,
                        "message": flowchart_message,
                        "size_bytes": os.path.getsize(flowchart_png_path) if flowchart_png_path and os.path.exists(
                            flowchart_png_path) else 0
                    }
                }
            },
            "file_info": {
                "text": {
                    "filename": filename_txt,
                    "filepath": file_path_txt,
                    "size_bytes": file_size_txt
                },
                "mindmap": {
                    "filename": f"mindmap_{timestamp}.png",
                    "filepath": mindmap_png_path,
                    "size_bytes": os.path.getsize(mindmap_png_path) if mindmap_png_path and os.path.exists(
                        mindmap_png_path) else 0
                } if mindmap_success else None,
                "flowchart": {
                    "filename": f"flowchart_{timestamp}.png",
                    "filepath": flowchart_png_path,
                    "size_bytes": os.path.getsize(flowchart_png_path) if flowchart_png_path and os.path.exists(
                        flowchart_png_path) else 0
                } if flowchart_success else None
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


