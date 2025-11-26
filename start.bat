@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: 💖 Emotional Counseling AI - 一键启动脚本
:: ============================================

echo.
echo ============================================
echo   💖 Emotional Counseling AI 启动脚本
echo   恋爱情绪咨询 AI 助手
echo ============================================
echo.

:: 获取脚本所在目录
cd /d "%~dp0"
set "PROJECT_DIR=%cd%"

:: ============================================
:: 环境检查
:: ============================================
echo [1/4] 🔍 检查运行环境...
echo.

:: 检查 Python
echo   检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ 错误: 未找到 Python
    echo   请安装 Python 3.9+ 并添加到系统 PATH
    echo   下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   ✅ Python %PYTHON_VERSION%

:: 检查 npm
echo   检查 Node.js/npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ 错误: 未找到 npm
    echo   请安装 Node.js 18+ 并添加到系统 PATH
    echo   下载地址: https://nodejs.org/
    pause
    exit /b 1
)
for /f %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
echo   ✅ npm %NPM_VERSION%

echo.
echo   ✅ 环境检查通过!
echo.

:: ============================================
:: 检查依赖是否安装
:: ============================================
echo [2/4] 📦 检查项目依赖...
echo.

:: 检查后端依赖
if not exist "%PROJECT_DIR%\backend\requirements.txt" (
    echo   ❌ 错误: 未找到 backend/requirements.txt
    pause
    exit /b 1
)
echo   ✅ 后端配置文件存在

:: 检查前端依赖
if not exist "%PROJECT_DIR%\frontend\package.json" (
    echo   ❌ 错误: 未找到 frontend/package.json
    pause
    exit /b 1
)

if not exist "%PROJECT_DIR%\frontend\node_modules" (
    echo   ⚠️  前端依赖未安装，正在安装...
    cd /d "%PROJECT_DIR%\frontend"
    npm install
    if %errorlevel% neq 0 (
        echo   ❌ 错误: 前端依赖安装失败
        pause
        exit /b 1
    )
    echo   ✅ 前端依赖安装完成
) else (
    echo   ✅ 前端依赖已安装
)

echo.

:: ============================================
:: 启动后端服务
:: ============================================
echo [3/4] 🚀 启动后端服务 (Flask, 端口 5000)...
echo.

cd /d "%PROJECT_DIR%"
start "Emotional AI - Backend (Port 5000)" cmd /k "cd /d %PROJECT_DIR%\backend && echo 💖 后端服务启动中... && echo. && python app.py"

:: 等待后端启动
echo   等待后端服务启动...
set BACKEND_READY=0
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    :: 尝试使用 curl，如果不可用则使用 PowerShell
    curl -s http://localhost:5000/api/health >nul 2>&1
    if !errorlevel! equ 0 (
        set BACKEND_READY=1
        goto backend_started
    )
    powershell -Command "try { $null = Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -UseBasicParsing -TimeoutSec 1; exit 0 } catch { exit 1 }" >nul 2>&1
    if !errorlevel! equ 0 (
        set BACKEND_READY=1
        goto backend_started
    )
    <nul set /p "=."
)
:backend_started
echo.

if %BACKEND_READY% equ 1 (
    echo   ✅ 后端服务已启动 - http://localhost:5000
) else (
    echo   ⚠️  后端服务可能仍在启动中，请检查后端窗口
)

echo.

:: ============================================
:: 启动前端服务
:: ============================================
echo [4/4] 🎨 启动前端服务 (Vite, 端口 3000)...
echo.

cd /d "%PROJECT_DIR%"
start "Emotional AI - Frontend (Port 3000)" cmd /k "cd /d %PROJECT_DIR%\frontend && echo 💖 前端服务启动中... && echo. && npm run dev"

:: 等待前端启动
echo   等待前端服务启动...
set FRONTEND_READY=0
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    :: 尝试使用 curl，如果不可用则使用 PowerShell
    curl -s http://localhost:3000 >nul 2>&1
    if !errorlevel! equ 0 (
        set FRONTEND_READY=1
        goto frontend_started
    )
    powershell -Command "try { $null = Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 1; exit 0 } catch { exit 1 }" >nul 2>&1
    if !errorlevel! equ 0 (
        set FRONTEND_READY=1
        goto frontend_started
    )
    <nul set /p "=."
)
:frontend_started
echo.

if %FRONTEND_READY% equ 1 (
    echo   ✅ 前端服务已启动 - http://localhost:3000
) else (
    echo   ⚠️  前端服务可能仍在启动中，请检查前端窗口
)

echo.

:: ============================================
:: 打开浏览器
:: ============================================
echo ============================================
echo   🎉 启动完成!
echo ============================================
echo.
echo   📍 前端地址: http://localhost:3000
echo   📍 后端地址: http://localhost:5000
echo.
echo   💡 提示:
echo   - 服务运行在新窗口中，关闭窗口即可停止对应服务
echo   - 或者运行 stop.bat 一键停止所有服务
echo.

:: 等待几秒后打开浏览器
timeout /t 2 /nobreak >nul
echo   🌐 正在打开浏览器...
start "" "http://localhost:3000"

echo.
echo   按任意键关闭此窗口（服务将继续运行）...
pause >nul
