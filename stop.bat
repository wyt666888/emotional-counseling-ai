@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Windows 停止脚本
:: ============================================================

title Emotional Counseling AI - 停止服务

echo.
echo ============================================================
echo    💖 Emotional Counseling AI - 停止服务
echo ============================================================
echo.

echo 此脚本将关闭所有相关的服务进程：
echo   - Python Flask 后端服务 (端口 5000)
echo   - Node.js Vite 前端服务 (端口 3000)
echo.

set /p confirm="确定要停止所有服务吗？(Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo [取消] 操作已取消
    pause
    exit /b 0
)

echo.
echo [停止] 正在停止服务...

:: 关闭占用 5000 端口的进程 (后端)
echo [清理] 正在关闭后端服务 (端口 5000)...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    if "%%a" neq "" if "%%a" neq "0" (
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo        已关闭进程 PID: %%a
        )
    )
)

:: 关闭占用 3000 端口的进程 (前端)
echo [清理] 正在关闭前端服务 (端口 3000)...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":3000 " ^| findstr "LISTENING"') do (
    if "%%a" neq "" if "%%a" neq "0" (
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo        已关闭进程 PID: %%a
        )
    )
)

:: 关闭标题包含后端服务的 CMD 窗口
echo [清理] 正在关闭服务窗口...
taskkill /FI "WINDOWTITLE eq Flask Backend - 后端服务" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Vite Frontend - 前端服务" /F >nul 2>&1

echo.
echo ============================================================
echo    ✅ 服务已停止
echo ============================================================
echo.
echo    所有服务进程已关闭。
echo    如需重新启动，请运行 start.bat
echo.
echo ============================================================
echo.

pause
