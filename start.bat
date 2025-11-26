@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Windows Startup Script
:: ============================================================

title Emotional Counseling AI - Starting...

echo.
echo ============================================================
echo    Emotional Counseling AI - Starting Services
echo ============================================================
echo.

:: Check Python environment
echo [CHECK] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found, please install Python 3.9+
    echo         Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python version: %PYTHON_VERSION%

:: Check Node.js environment
echo [CHECK] Checking Node.js environment...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found, please install Node.js 18+
    echo         Download: https://nodejs.org/
    pause
    exit /b 1
)
for /f %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo [OK] Node.js version: %NODE_VERSION%

:: Check npm environment
echo [CHECK] Checking npm environment...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found, please check Node.js installation
    pause
    exit /b 1
)
for /f %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
echo [OK] npm version: %NPM_VERSION%

echo.
echo ============================================================
echo    Starting services...
echo ============================================================
echo.

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check backend directory
if not exist "backend\app.py" (
    echo [ERROR] Backend file not found: backend\app.py
    echo         Please run this script from the project root directory
    pause
    exit /b 1
)

:: Check frontend directory
if not exist "frontend\package.json" (
    echo [ERROR] Frontend file not found: frontend\package.json
    echo         Please run this script from the project root directory
    pause
    exit /b 1
)

:: Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo [INFO] First run, installing frontend dependencies...
    cd frontend
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Frontend dependency installation failed
        pause
        exit /b 1
    )
    cd ..
    echo [OK] Frontend dependencies installed
)

:: Start backend service
echo [START] Starting backend service (port 5000)...
start "Flask Backend" cmd /k "cd /d %SCRIPT_DIR%backend && python app.py"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start backend service
    pause
    exit /b 1
)

:: Wait for backend service to start
echo [WAIT] Waiting for backend service to start...
set /a count=0
:wait_backend
timeout /t 1 >nul
set /a count+=1
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend service started
    goto backend_ready
)
if %count% geq 30 (
    echo [WARN] Backend service startup timeout, continuing with frontend...
    goto backend_ready
)
goto wait_backend

:backend_ready

:: Start frontend service
echo [START] Starting frontend service (port 5173)...
start "Vite Frontend" cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start frontend service
    pause
    exit /b 1
)

:: Wait for frontend service to start
echo [WAIT] Waiting for frontend service to start...
set /a count=0
:wait_frontend
timeout /t 1 >nul
set /a count+=1
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5173' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Frontend service started
    goto frontend_ready
)
if %count% geq 30 (
    echo [WARN] Frontend service startup timeout, trying to open browser...
    goto frontend_ready
)
goto wait_frontend

:frontend_ready

:: Wait to ensure services are stable
timeout /t 2 >nul

:: Open browser
echo.
echo [OPEN] Opening browser...
start "" http://localhost:5173

echo.
echo ============================================================
echo    Startup complete!
echo ============================================================
echo.
echo    Backend:  http://localhost:5000
echo    Frontend: http://localhost:5173
echo.
echo    Tips:
echo    - Keep both service windows open
echo    - To stop services, run stop.bat
echo    - Or close the service windows directly
echo.
echo ============================================================
echo.

pause
