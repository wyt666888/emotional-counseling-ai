@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: 💖 Emotional Counseling AI - 停止脚本
:: ============================================

echo.
echo ============================================
echo   💖 Emotional Counseling AI 停止脚本
echo   恋爱情绪咨询 AI 助手
echo ============================================
echo.

:: ============================================
:: 确认操作
:: ============================================
echo   ⚠️  此操作将停止以下服务:
echo   - 后端 Flask 服务 (端口 5000)
echo   - 前端 Vite 服务 (端口 3000)
echo.
set /p "CONFIRM=确定要停止所有服务吗? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo.
    echo   ❌ 操作已取消
    pause
    exit /b 0
)

echo.
echo ============================================
echo   🔄 正在停止服务...
echo ============================================
echo.

set STOPPED_COUNT=0

:: ============================================
:: 停止后端服务 (Python/Flask)
:: ============================================
echo [1/2] 🐍 停止后端服务...

:: 查找并关闭占用 5000 端口的进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING" 2^>nul') do (
    set "PID=%%a"
    if not "!PID!"=="" (
        taskkill /PID !PID! /F >nul 2>&1
        if !errorlevel! equ 0 (
            echo   ✅ 已停止后端进程 (PID: !PID!)
            set /a STOPPED_COUNT+=1
        )
    )
)

:: 查找并关闭 python app.py 进程
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST 2^>nul ^| findstr "PID:"') do (
    set "PID=%%a"
    :: 检查是否是我们的应用进程
    wmic process where "ProcessId=!PID!" get CommandLine 2>nul | findstr /i "app.py" >nul 2>&1
    if !errorlevel! equ 0 (
        taskkill /PID !PID! /F >nul 2>&1
        if !errorlevel! equ 0 (
            echo   ✅ 已停止 Python 进程 (PID: !PID!)
            set /a STOPPED_COUNT+=1
        )
    )
)

echo   ✅ 后端服务检查完成
echo.

:: ============================================
:: 停止前端服务 (Node.js/Vite)
:: ============================================
echo [2/2] 🎨 停止前端服务...

:: 查找并关闭占用 3000 端口的进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000" ^| findstr "LISTENING" 2^>nul') do (
    set "PID=%%a"
    if not "!PID!"=="" (
        taskkill /PID !PID! /F >nul 2>&1
        if !errorlevel! equ 0 (
            echo   ✅ 已停止前端进程 (PID: !PID!)
            set /a STOPPED_COUNT+=1
        )
    )
)

:: 查找并关闭 node 相关进程（vite）
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq node.exe" /FO LIST 2^>nul ^| findstr "PID:"') do (
    set "PID=%%a"
    :: 检查是否是 vite 进程
    wmic process where "ProcessId=!PID!" get CommandLine 2>nul | findstr /i "vite" >nul 2>&1
    if !errorlevel! equ 0 (
        taskkill /PID !PID! /F >nul 2>&1
        if !errorlevel! equ 0 (
            echo   ✅ 已停止 Node 进程 (PID: !PID!)
            set /a STOPPED_COUNT+=1
        )
    )
)

echo   ✅ 前端服务检查完成
echo.

:: ============================================
:: 清理相关 CMD 窗口
:: ============================================
echo [*] 🧹 清理服务窗口...

:: 关闭标题包含 "Emotional AI" 的窗口
:: 注意: 这些窗口标题必须与 start.bat 中设置的标题保持一致
:: start.bat 中设置的标题: "Emotional AI - Backend (Port 5000)" 和 "Emotional AI - Frontend (Port 3000)"
taskkill /FI "WINDOWTITLE eq Emotional AI - Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Emotional AI - Frontend*" /F >nul 2>&1

echo   ✅ 清理完成
echo.

:: ============================================
:: 完成提示
:: ============================================
echo ============================================
echo   🎉 操作完成!
echo ============================================
echo.

if %STOPPED_COUNT% gtr 0 (
    echo   已停止 %STOPPED_COUNT% 个相关进程
) else (
    echo   未发现运行中的服务进程
)

echo.
echo   💡 提示: 运行 start.bat 可重新启动服务
echo.

pause
