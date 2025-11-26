@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Windows 一键启动脚本
:: ============================================================

title Emotional Counseling AI - 启动中...

echo.
echo ============================================================
echo    💖 Emotional Counseling AI - 恋爱情绪咨询 AI
echo ============================================================
echo.

:: 检查 Python 环境
echo [检查] 正在检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    echo        下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [成功] Python 版本: %PYTHON_VERSION%

:: 检查 Node.js 环境
echo [检查] 正在检查 Node.js 环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    echo        下载地址: https://nodejs.org/
    pause
    exit /b 1
)
for /f %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo [成功] Node.js 版本: %NODE_VERSION%

:: 检查 npm 环境
echo [检查] 正在检查 npm 环境...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 npm，请检查 Node.js 安装
    pause
    exit /b 1
)
for /f %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
echo [成功] npm 版本: %NPM_VERSION%

echo.
echo ============================================================
echo    正在启动服务...
echo ============================================================
echo.

:: 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: 检查后端目录
if not exist "backend\app.py" (
    echo [错误] 未找到后端文件 backend\app.py
    echo        请确保在正确的项目目录下运行此脚本
    pause
    exit /b 1
)

:: 检查前端目录
if not exist "frontend\package.json" (
    echo [错误] 未找到前端文件 frontend\package.json
    echo        请确保在正确的项目目录下运行此脚本
    pause
    exit /b 1
)

:: 检查前端依赖是否已安装
if not exist "frontend\node_modules" (
    echo [提示] 首次运行，正在安装前端依赖...
    cd frontend
    npm install
    if %errorlevel% neq 0 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
    cd ..
    echo [成功] 前端依赖安装完成
)

:: 启动后端服务
echo [启动] 正在启动后端服务 (端口 5000)...
start "Flask Backend - 后端服务" cmd /k "cd /d %SCRIPT_DIR%backend && python app.py"

:: 等待后端服务启动
echo [等待] 等待后端服务启动...
set /a count=0
:wait_backend
timeout /t 1 >nul
set /a count+=1
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] 后端服务已启动
    goto backend_ready
)
if %count% geq 30 (
    echo [警告] 后端服务启动超时，继续启动前端...
    goto backend_ready
)
goto wait_backend

:backend_ready

:: 启动前端服务
echo [启动] 正在启动前端服务 (端口 3000)...
start "Vite Frontend - 前端服务" cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"

:: 等待前端服务启动
echo [等待] 等待前端服务启动...
set /a count=0
:wait_frontend
timeout /t 1 >nul
set /a count+=1
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [成功] 前端服务已启动
    goto frontend_ready
)
if %count% geq 30 (
    echo [警告] 前端服务启动超时，尝试打开浏览器...
    goto frontend_ready
)
goto wait_frontend

:frontend_ready

:: 等待一下确保服务稳定
timeout /t 2 >nul

:: 打开浏览器
echo.
echo [打开] 正在打开浏览器...
start "" http://localhost:3000

echo.
echo ============================================================
echo    🎉 启动完成！
echo ============================================================
echo.
echo    后端服务: http://localhost:5000
echo    前端界面: http://localhost:3000
echo.
echo    提示:
echo    - 请保持两个服务窗口处于打开状态
echo    - 关闭服务请运行 stop.bat
echo    - 或直接关闭服务窗口
echo.
echo ============================================================
echo.

pause
