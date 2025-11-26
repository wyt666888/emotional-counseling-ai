@echo off
echo Starting Emotional Counseling AI...
echo.

cd /d "%~dp0"

echo Starting backend...
start "Backend" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak

echo Starting frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 5 /nobreak

echo Opening browser...
start http://localhost:5173

echo.
echo Services started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
pause
