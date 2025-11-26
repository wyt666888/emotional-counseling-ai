@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Stop Script
:: ============================================================

title Emotional Counseling AI - Stopping Services

echo.
echo ============================================================
echo    Emotional Counseling AI - Stop Services
echo ============================================================
echo.

echo This script will close all related service processes:
echo   - Python Flask backend (port 5000)
echo   - Node.js Vite frontend (ports 3000/3001/3002/5173)
echo.

set /p confirm="Are you sure you want to stop all services? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo.
    echo [CANCEL] Operation cancelled
    pause
    exit /b 0
)

echo.
echo [STOP] Stopping services...

:: Close backend process (port 5000)
echo [CLEAN] Stopping backend service (port 5000)...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    if "%%a" neq "" if "%%a" neq "0" (
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo         Closed process PID: %%a
        )
    )
)

:: Close frontend processes (ports 3000, 3001, 3002, 5173)
echo [CLEAN] Stopping frontend services (ports 3000/3001/3002/5173)...
for %%p in (3000 3001 3002 5173) do (
    for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":%%p " ^| findstr "LISTENING"') do (
        if "%%a" neq "" if "%%a" neq "0" (
            taskkill /F /PID %%a >nul 2>&1
            if !errorlevel! equ 0 (
                echo         Closed process on port %%p, PID: %%a
            )
        )
    )
)

:: Close service windows by title
echo [CLEAN] Closing service windows...
taskkill /FI "WINDOWTITLE eq Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend*" /F >nul 2>&1

echo.
echo ============================================================
echo    Services Stopped
echo ============================================================
echo.
echo    All service processes have been closed.
echo    Run start.bat to restart the services.
echo.
echo ============================================================
echo.

pause
