@echo off
echo Stopping SmartPack processes...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /IM uvicorn.exe /T >nul 2>&1
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr "8000" ') DO taskkill /F /PID %%T /T >nul 2>&1
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr "5173" ') DO taskkill /F /PID %%T /T >nul 2>&1
echo Done.
