import threading
import asyncio
from typing import Optional
from fastapi.responses import FileResponse
import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os
from urllib.parse import unquote

from pymysql.cursors import DictCursor

# ========================
# Agent 导入（替代旧的散落文件）
# ========================
from agents.teaching_plan_agent import TeachingPlanAgent
from agents.qa_agent import QAAgent
from agents.question_gen_agent import QuestionGenAgent
from agents.student_practice_agent import StudentPracticeAgent
from agents.exam_process_agent import ExamProcessAgent
from agents.exam_analysis_agent import ExamAnalysisAgent
from agents.knowledge_graph_agent import KnowledgeGraphAgent, DBChangeListener
from document import DocumentProcessor
from dotenv import load_dotenv

from fastapi import UploadFile, File
load_dotenv()

# 创建 FastAPI 应用
app = FastAPI()

# 允许跨域（Vue 前端访问）
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# 初始化 Agent 实例
# ========================
teaching_plan_agent = TeachingPlanAgent()
qa_agent = QAAgent()
question_gen_agent = QuestionGenAgent()
student_practice_agent = StudentPracticeAgent()
exam_process_agent = ExamProcessAgent()
exam_analysis_agent = ExamAnalysisAgent()
knowledge_graph_agent = KnowledgeGraphAgent()

# ========================
# 启动信息打印
# ========================
_current_provider = os.getenv("LLM_PROVIDER", "dashscope")
print(f"\n{'='*50}")
print(f"  教育平台 AI 服务已启动")
print(f"  当前大模型通道: {_current_provider.upper()}")
if _current_provider == "iflytek":
    print(f"  讯飞模型版本: {os.getenv('IFLYTEK_MODEL_VERSION', 'generalv3.5')}")
    print(f"  讯飞 APP_ID:  {os.getenv('IFLYTEK_APP_ID', '未配置')}")
else:
    print(f"  通义千问模型: {os.getenv('LLM_MODEL', 'qwen-turbo')}")
print(f"  服务地址: http://0.0.0.0:8000")
print(f"{'='*50}\n")

# 请求体模型
class CourseOutlineRequest(BaseModel):
    name: str
    content: str
class QuestionRequest(BaseModel):
    question: str
    context: str
class QuestionGenerateRequest(BaseModel):
    prompt: str
class QuestionRequest_stu(BaseModel):
    prompt: str
class AnswerGradeRequest(BaseModel):
    question: str
    question_type: str
    student_answer: str

class MultimodalRequest(BaseModel):
    topic: str
    difficulty: str = "standard"
    preference: str = "theory"

class FileResponseModel(BaseModel):
    content: dict
    file_name: str
    file_type: str
class ExamProcessingResponse(BaseModel):
    success: bool
    message: str
    answer_file: Optional[str] = None
    rubric_file: Optional[str] = None

class ExamAnalysisResponse(BaseModel):
    success: bool
    message: str
    report_path: Optional[str] = None
class KnowledgeGraphRequest(BaseModel):
    user_id: Optional[int] = None

@app.post("/generate-course")
async def generate_course(request: CourseOutlineRequest):
    course_data = {
        "name": request.name,
        "content": request.content
    }

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: teaching_plan_agent.process(course_outline=course_data)
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("message", "未知错误"))

    return result

@app.post("/ask-question")
async def ask_question(request: QuestionRequest):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: qa_agent.process(question=request.question, context=request.context)
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("message", "未知错误"))

    return result

@app.post("/generate-question")
async def generate_question_endpoint(request: QuestionGenerateRequest):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: question_gen_agent.process(prompt=request.prompt)
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("message", "题目生成失败，请检查日志或重试"))

    return result["data"]

# ========================
# 接口1：生成题目
# ========================

@app.post("/question/generate")
async def generate_question_endpoint(request: QuestionRequest_stu):
    """
    根据提示词生成题目
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: student_practice_agent.process(action="generate", prompt=request.prompt)
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "题目生成失败，请检查日志或重试")
        )
    return result["data"]


# ========================
# 接口2：批改作业
# ========================

@app.post("/question/grade")
async def grade_answer_endpoint(request: AnswerGradeRequest):
    """
    对学生作答进行自动批改
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: student_practice_agent.process(
            action="grade",
            question=request.question,
            student_answer=request.student_answer,
            question_type=request.question_type
        )
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "批改失败")
        )

    return result["data"]

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    allowed_types = ['.docx', '.xlsx', '.txt']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型 {file_extension}"
        )

    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        processor = DocumentProcessor(file_path)
        result = processor.process()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")
    finally:
        os.remove(file_path)

    return {"filename": file.filename, "content": result}


@app.post("/process-exam")
async def process_exam(file: UploadFile = File(...)):
    # 检查文件类型
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型 {file_ext}. 仅支持: {', '.join(allowed_extensions)}"
        )

    # 创建临时目录
    temp_dir = "temp_exams"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    # 保存上传的文件
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件保存失败: {str(e)}"
        )

    # 处理试卷（通过 Agent）
    result = exam_process_agent.process(file_path=temp_path)

    # 清理临时文件
    try:
        os.remove(temp_path)
    except:
        pass

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result.get("message", "试卷处理失败")
        )

    # 构建响应
    data = result["data"]
    response = {
        "success": True,
        "message": "试卷处理完成",
        "answer_file": data["answer_file"],
        "answer_size": data["answer_size"],
        "rubric_file": data["rubric_file"],
        "rubric_size": data["rubric_size"]
    }

    return response


@app.post("/analyze-exam")
async def analyze_exam(file: UploadFile = File(...)):
    """
    处理上传的考试成绩Excel文件，生成试卷分析报告
    """
    # 检查文件类型
    if not file.filename.lower().endswith('.xlsx'):
        raise HTTPException(
            status_code=400,
            detail="仅支持.xlsx格式的Excel文件"
        )

    # 创建临时目录
    temp_dir = "temp_analysis"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    # 保存上传的文件
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件保存失败: {str(e)}"
        )

    # 处理试卷分析（通过 Agent）
    result = exam_analysis_agent.process(file_path=temp_path)

    # 清理临时文件
    try:
        os.remove(temp_path)
    except:
        pass

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result.get("message", "试卷分析报告生成失败")
        )

    # 构建响应
    data = result["data"]
    response = {
        "success": True,
        "message": "试卷分析报告生成成功",
        "report_path": data["report_path"],
        "report_filename": data["report_filename"],
        "report_size": data["report_size"]
    }
    return response

# 文件下载接口
@app.get("/download-file/{filename}")
async def download_file(filename: str):
    """
    下载生成的文件（支持中文文件名）
    """
    try:
        decoded_filename = unquote(filename)

        if ".." in decoded_filename or "/" in decoded_filename or "\\" in decoded_filename:
            raise HTTPException(status_code=400, detail="无效的文件名")

        file_path = os.path.join("output", decoded_filename)

        if not os.path.exists(file_path):
            file_path = os.path.join("temp_analysis", decoded_filename)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"文件不存在: {decoded_filename}"
            )

        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=decoded_filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件下载失败: {str(e)}"
        )


@app.get("/user-knowledge-mastery")
async def get_user_knowledge_mastery(user_id: Optional[str] = None):
    """
    获取用户的知识点掌握度数据
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="缺少 user_id 参数")

    try:
        mastery = KnowledgeGraphAgent.get_user_knowledge_mastery(user_id)
        return {
            "success": True,
            "mastery": mastery
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取掌握度数据失败：{str(e)}"
        )


@app.get("/knowledge-graph")
async def get_knowledge_graph(user_id: Optional[int] = None):
    """
    获取知识图谱数据
    """
    try:
        graph = KnowledgeGraphAgent.get_knowledge_graph_from_db(user_id)
        return {
            "success": True,
            "graph": graph
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取知识图谱失败: {str(e)}"
        )


# 在FastAPI启动时启动监听器
@app.on_event("startup")
async def startup_event():
    # 启动后台监听器（新版 DBChangeListener 不再需要 db_config 参数）
    listener = DBChangeListener()
    listener_thread = threading.Thread(target=listener.start, daemon=True)
    listener_thread.start()


@app.post("/generate-mindmap")
async def generate_mindmap(request: MultimodalRequest):
    """生成思维导图数据结构（Markmap 格式）"""
    prompt = f"""请针对"{request.topic}"这个知识点，生成一个思维导图的JSON结构。
难度级别：{request.difficulty}
要求：
1. 以JSON格式返回，包含root（中心主题）和children（子主题数组）
2. 每个子主题可以有children形成多层级
3. 内容要专业、准确，适合教学使用
4. 至少包含3个层级，总共8-15个节点

返回格式示例：
{{"root": "核心主题", "children": [{{"name": "子主题1", "children": [{{"name": "知识点1.1"}}, {{"name": "知识点1.2"}}]}}, {{"name": "子主题2", "children": [{{"name": "知识点2.1"}}]}}]}}

请直接返回JSON，不要其他文字。"""
    try:
        from agents.qa_agent import QAAgent
        agent = QAAgent()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: agent.process(question=prompt, context="")
        )
        if result["success"]:
            return {"success": True, "data": result["data"]["answer"]}
        else:
            raise HTTPException(status_code=500, detail=result.get("message", "生成失败"))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成思维导图失败: {str(e)}")



@app.post("/generate-code-examples")
async def generate_code_examples(request: MultimodalRequest):
    """根据难度级别生成对应代码案例"""
    level_map = {
        "basic": ("基础版", "适合初学者的简单示例，代码简洁易懂，有详细注释"),
        "standard": ("标准版", "包含常用特性和最佳实践的示例，有适当注释"),
        "advanced": ("进阶版", "展示高级用法和设计模式的示例，注释精炼"),
    }
    level_title, level_desc = level_map.get(request.difficulty, level_map["standard"])

    code_prompt = f"""请为"{request.topic}"生成一个{level_title}的Python代码案例。
难度说明：{level_desc}

要求：
1. 代码完整可运行，包含中文注释
2. 难度符合{request.difficulty}级别
3. 只输出代码，不要任何解释文字，不要用代码包裹"""

    try:
        agent = QAAgent()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: agent.adapter.call(
                prompt=code_prompt,
                system_prompt="你是一个代码生成器。只输出纯代码，不输出任何解释、说明、标题或代码格式。"
            )
        )
        if result.success:
            import re
            code_clean = result.content.strip()
            code_clean = re.sub(r'^```(?:\w+)?\s*\n?', '', code_clean)
            code_clean = re.sub(r'\n?\s*```$', '', code_clean)
            code_clean = code_clean.strip()
            return {"success": True, "data": {
                "title": level_title,
                "description": level_desc,
                "code": code_clean,
                "language": "python"
            }}
        else:
            raise HTTPException(status_code=500, detail=result.error_message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成代码案例失败: {str(e)}")

@app.post("/generate-practice-questions")
async def generate_practice_questions(request: MultimodalRequest):
    """生成专项练习题库"""
    prompt = f"""请针对"{request.topic}"这个知识点，生成一套专项练习题。
难度级别：{request.difficulty}

要求：
1. 恰好生成10道题目
2. 题型由你根据知识点特点自行决定，可以从选择题、判断题、填空题、简答题中自由搭配，不必每种都有，怎么合理怎么来
3. 题目要有针对性，覆盖该知识点的核心内容
4. 难度要适中，符合{request.difficulty}级别
5. 直接返回JSON，不要其他文字

请按以下JSON格式返回：
{{
  "questions": [
    {{
      "id": 1,
      "type": "choice/judge/fill/essay",
      "question": "题目内容",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "answer": "答案",
      "explanation": "解析说明"
    }}
  ]
}}

注意：
- type 为 choice 时需提供 options 字段（四个选项）
- type 为 judge 时不需要 options，answer 填"正确"或"错误"
- type 为 fill 时不需要 options，answer 填正确答案
- type 为 essay 时不需要 options，answer 填参考答案要点"""
    try:
        from agents.qa_agent import QAAgent
        agent = QAAgent()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: agent.process(question=prompt, context="")
        )
        if result["success"]:
            return {"success": True, "data": result["data"]["answer"]}
        else:
            raise HTTPException(status_code=500, detail=result.get("message", "生成失败"))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成练习题失败: {str(e)}")


@app.post("/generate-analysis-report")
async def generate_analysis_report(request: MultimodalRequest):
    """生成完整文字解析报告"""
    prompt = f"""请针对"{request.topic}"这个知识点，生成一份完整的文字解析报告。
难度级别：{request.difficulty}
输出偏好：{request.preference}

报告应包含以下部分，用Markdown格式返回：

# {request.topic} 知识点解析报告

## 一、概念定义
（清晰准确地定义该知识点）

## 二、核心原理
（深入讲解工作原理和机制）

## 三、关键特性
（列出3-5个关键特性，每个特性配简要说明）

## 四、应用场景
（列举2-3个实际应用场景）

## 五、常见误区
（指出学习者容易犯的错误和误解）

## 六、学习建议
（给出针对性的学习路径和建议）

要求：
1. 内容专业准确，适合教学
2. 语言通俗易懂
3. 适当使用加粗、列表等Markdown格式
4. 总字数800-1500字"""
    try:
        from agents.qa_agent import QAAgent
        agent = QAAgent()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: agent.process(question=prompt, context="")
        )
        if result["success"]:
            return {"success": True, "data": result["data"]["answer"]}
        else:
            raise HTTPException(status_code=500, detail=result.get("message", "生成失败"))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成解析报告失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
