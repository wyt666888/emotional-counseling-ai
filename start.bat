@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: Emotional Counseling AI - Smart Start Script
:: ============================================================

title Emotional Counseling AI - Starting...

echo.
echo ============================================================
echo    Emotional Counseling AI - Smart Start Script
echo ============================================================
echo.

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Check Python environment
echo [CHECK] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+
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
    echo [ERROR] Node.js not found. Please install Node.js 18+
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
    echo [ERROR] npm not found. Please check Node.js installation
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
    echo [INFO] First run - Installing frontend dependencies...
    echo        This may take a few minutes, please wait...
    cd frontend
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Frontend dependency installation failed
        pause
        exit /b 1
    )
    cd ..
    echo [OK] Frontend dependencies installed successfully
    echo.
)

:: Start backend service
echo [START] Starting backend service (port 5000)...
start "Backend - Flask Server" cmd /k "cd /d "%SCRIPT_DIR%backend" && python app.py"

:: Wait for backend to start
echo [WAIT] Waiting for backend service to start...
set /a count=0
:wait_backend
timeout /t 1 >nul
set /a count+=1
netstat -ano 2>nul | findstr "LISTENING" | findstr ":5000 " >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend service started on port 5000
    goto backend_ready
)
if %count% geq 15 (
    echo [WARN] Backend startup timeout, continuing with frontend...
    goto backend_ready
)
goto wait_backend

:backend_ready
echo.

:: Start frontend service
echo [START] Starting frontend service (Vite will auto-select available port)...
start "Frontend - Vite Server" cmd /k "cd /d "%SCRIPT_DIR%frontend" && npm run dev"

:: Wait for frontend to start and detect actual port
echo [WAIT] Waiting for frontend service to start...
timeout /t 5 >nul

:: Smart port detection - check common Vite ports
echo [DETECT] Detecting frontend port...
set "FRONTEND_PORT="

:: Check ports in order: 3000, 3001, 3002, 5173
for %%p in (3000 3001 3002 5173) do (
    if not defined FRONTEND_PORT (
        netstat -ano 2>nul | findstr "LISTENING" | findstr ":%%p " >nul 2>&1
        if !errorlevel! equ 0 (
            set "FRONTEND_PORT=%%p"
            echo [OK] Frontend service detected on port %%p
        )
    )
)

:: If no port found, wait a bit more and try again
if not defined FRONTEND_PORT (
    echo [WAIT] Frontend not ready yet, waiting 5 more seconds...
    timeout /t 5 >nul
    for %%p in (3000 3001 3002 5173) do (
        if not defined FRONTEND_PORT (
            netstat -ano 2>nul | findstr "LISTENING" | findstr ":%%p " >nul 2>&1
            if !errorlevel! equ 0 (
                set "FRONTEND_PORT=%%p"
                echo [OK] Frontend service detected on port %%p
            )
        )
    )
)

echo.

:: Open browser with detected port
if defined FRONTEND_PORT (
    echo [OPEN] Opening browser at http://localhost:!FRONTEND_PORT!
    start "" http://localhost:!FRONTEND_PORT!
) else (
    echo [WARN] Could not auto-detect frontend port
    echo        Please check the Frontend window for the actual URL
    echo        Common URLs: http://localhost:3000 or http://localhost:3001
)

echo.
echo ============================================================
echo    Startup Complete!
echo ============================================================
echo.
echo    Backend:  http://localhost:5000
if defined FRONTEND_PORT (
    echo    Frontend: http://localhost:!FRONTEND_PORT!
) else (
    echo    Frontend: Check the Frontend window for actual URL
)
echo.
echo    Tips:
echo    - Keep both service windows open
echo    - Run stop.bat to stop all services
echo    - Or close the service windows directly
echo.
echo ============================================================
echo.

pause
