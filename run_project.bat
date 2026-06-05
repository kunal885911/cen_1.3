@echo off
echo ===================================================
echo Starting CAD Automation System v1.0...
echo ===================================================

echo.
echo [1/2] Starting FastAPI Backend...
start cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [2/2] Starting React/Vite Frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo Servers are booting up in separate windows!
echo - Frontend: http://localhost:5173
echo - Backend:  http://localhost:8000
echo.
echo You can close this window now. Keep the other windows open to keep the servers running.
pause
