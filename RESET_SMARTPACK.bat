@echo off
setlocal EnableDelayedExpansion

echo ==================================================
echo         SMARTPACK AI - RESET ORCHESTRATOR
echo ==================================================
echo.
echo WARNING: This will destroy all current data and reset the system to a clean demo state.
echo Press Ctrl+C to abort, or any key to continue...
pause >nul
echo.

echo Stopping services...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1

echo Removing database...
if exist "smartpack.db" del smartpack.db

echo Regenerating demo dataset...
call venv\Scripts\activate.bat
python scripts/generate_demo_dataset.py

echo Reinitializing database and seeding data...
python -m backend.app.seed.seed_database

echo.
echo Reset complete. You can now run START_SMARTPACK.bat.
pause
