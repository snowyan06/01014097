# quick_start.ps1
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  教育平台快速启动" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

$projectRoot = $PSScriptRoot

Write-Host "[1/4] 启动 Java 后端 (端口 8080)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$projectRoot\Edu_platform'
Write-Host ' 启动 Java 后端...' -ForegroundColor Cyan
mvn spring-boot:run
"@

Start-Sleep -Seconds 5

Write-Host "[2/4] 启动 AI 数字人 (端口 8010)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$projectRoot\avatar_py'
Write-Host ' 启动 AI 数字人服务...' -ForegroundColor Cyan
python app.py --model musetalk --transport webrtc
"@

Start-Sleep -Seconds 5

Write-Host "[3/4] 启动 Python AI (端口 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$projectRoot\Edu_py'
Write-Host ' 启动 Python AI 服务...' -ForegroundColor Cyan
python main.py
"@

Start-Sleep -Seconds 3

Write-Host "[4/4] 启动前端 (端口 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$projectRoot\EduGenius'
Write-Host ' 启动前端服务...' -ForegroundColor Cyan
npm run dev
"@

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  服务启动完成！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host " 访问地址:" -ForegroundColor Cyan
Write-Host "   前端：http://localhost:5173" -ForegroundColor White
Write-Host "   登录：http://localhost:5173/auth/login" -ForegroundColor White
Write-Host "   注册：http://localhost:5173/register" -ForegroundColor White
Write-Host "   数字人：http://localhost:8010/webrtcapi.html" -ForegroundColor White

Write-Host "  WebRTC 信令服务器 (数字人语音对话):" -ForegroundColor Yellow
Write-Host "  需要手动启动，执行以下命令:" -ForegroundColor White
Write-Host "  cd '$projectRoot\avatar_py'" -ForegroundColor Gray
Write-Host "  .\avatar_env\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  python webrtc_server_simple.py --port 7860" -ForegroundColor Gray
Write-Host ""
Write-Host "  停止服务：关闭所有 PowerShell 窗口" -ForegroundColor Gray
Write-Host ""

Start-Sleep -Seconds 10
Write-Host "正在打开浏览器..." -ForegroundColor Cyan
Start-Process "http://localhost:5173/auth/login"
