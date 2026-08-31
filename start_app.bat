@echo off
title MediCore Nexus Platform Launcher
echo ======================================================================
echo           Starting MediCore Nexus Healthcare Platform
echo ======================================================================
echo.

echo [1/2] Starting Python FastAPI Backend Server on port 8000...
start "MediCore Backend" cmd /k "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Vite Frontend Server on port 5173...
start "MediCore Frontend" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo Opening browser at http://localhost:5173/ ...
start http://localhost:5173/

echo.
echo ======================================================================
echo MediCore Nexus is now running!
echo Frontend: http://localhost:5173/
echo Backend API: http://localhost:8000/api/v1/health
echo ======================================================================
pause
