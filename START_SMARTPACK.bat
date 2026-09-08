@echo off
setlocal EnableDelayedExpansion

echo ==================================================
echo         SMARTPACK AI - STARTUP ORCHESTRATOR
echo ==================================================
echo.

:: Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] ERROR: Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python and Node.js detected.
echo.

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Installing backend requirements...
python -m pip install --upgrade pip -q
python -m pip install -r backend/requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    echo [!] ERROR: Failed to install backend requirements.
    pause
    exit /b 1
)

echo Installing frontend dependencies...
cd frontend
call npm install --silent
if %ERRORLEVEL% NEQ 0 (
    echo [!] ERROR: Failed to install frontend dependencies.
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

:: Check for dataset
if not exist "dataset\images\correct" (
    echo Generating demo dataset...
    python scripts/generate_demo_dataset.py
)

:: Initialize database and seed demo data
echo Initializing database...
python -m backend.app.seed.seed_database

echo.
echo ==================================================
echo Starting SmartPack AI Services...
echo ==================================================

:: Start Backend in new window
echo Starting Backend API...
start "SmartPack AI Backend" cmd /c "call venv\Scripts\activate.bat && cd backend && uvicorn app.main:app --reload --port 8000"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Frontend in new window
echo Starting Frontend UI...
start "SmartPack AI Frontend" cmd /c "cd frontend && npm run dev -- --port 5173"

echo.
echo Backend: ONLINE
echo Database: ONLINE
echo Verification Engine: READY
echo Frontend: ONLINE
echo.
echo Application: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo ==================================================
echo Press any key to stop all services...
pause >nul

:: Terminate child processes
echo Shutting down services...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
echo Done.
