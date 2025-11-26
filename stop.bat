@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Windows Stop Script
:: ============================================================

title Emotional Counseling AI - Stop Services

echo.
echo ============================================================
echo    Emotional Counseling AI - Stop Services
echo ============================================================
echo.

echo This script will close all related service processes:
echo   - Python Flask backend service (port 5000)
echo   - Node.js Vite frontend service (port 5173)
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

:: Close processes using port 5000 (backend)
echo [CLEAN] Closing backend service (port 5000)...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    if "%%a" neq "" if "%%a" neq "0" (
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo         Closed process PID: %%a
        )
    )
)

:: Close processes using port 5173 (frontend)
echo [CLEAN] Closing frontend service (port 5173)...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":5173 " ^| findstr "LISTENING"') do (
    if "%%a" neq "" if "%%a" neq "0" (
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo         Closed process PID: %%a
        )
    )
)

:: Close CMD windows with service titles
echo [CLEAN] Closing service windows...
taskkill /FI "WINDOWTITLE eq Flask Backend" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Vite Frontend" /F >nul 2>&1

echo.
echo ============================================================
echo    Services stopped
echo ============================================================
echo.
echo    All service processes have been closed.
echo    To restart, run start.bat
echo.
echo ============================================================
echo.

pause
