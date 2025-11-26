@echo off
:: ============================================================
:: Emotional Counseling AI - Simple Start Script
:: A minimal script without port detection
:: ============================================================

echo.
echo ============================================================
echo    Emotional Counseling AI - Simple Start
echo ============================================================
echo.

cd /d "%~dp0"

:: Check basic requirements
if not exist "backend\app.py" (
    echo [ERROR] Backend not found. Run from project root directory.
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo [ERROR] Frontend not found. Run from project root directory.
    pause
    exit /b 1
)

:: Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo [START] Starting backend on port 5000...
start "Backend" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul

echo [START] Starting frontend (auto-select port)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo    Services started!
echo ============================================================
echo.
echo    - Backend:  http://localhost:5000
echo    - Frontend: Check the Frontend window for actual URL
echo               (Usually http://localhost:3000 or :3001)
echo.
echo    Tips:
echo    - Keep both service windows open
echo    - Run stop.bat to stop all services
echo.
echo ============================================================
echo.

pause
