@echo off
cd /d C:\Users\lenovo\IdeaProjects\01014097
echo [1/3] 安装依赖... > run_result.txt
pip install python-docx >> run_result.txt 2>&1
echo [2/3] 生成文档... >> run_result.txt
python generate_doc.py >> run_result.txt 2>&1
echo [3/3] 检查结果... >> run_result.txt
if exist "EduGenius_技术文档.docx" (
    echo 成功！文档已生成：EduGenius_技术文档.docx >> run_result.txt
    dir EduGenius_技术文档.docx >> run_result.txt
) else (
    echo 失败！请查看上方错误信息 >> run_result.txt
)
type run_result.txt
