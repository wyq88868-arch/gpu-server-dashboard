@echo off
setlocal
title Close Dashboard Local Ports

echo ============================================================
echo Closing local dashboard ports: 8765 and 8766
echo ============================================================
echo.

for %%P in (8765 8766) do (
    echo Checking port %%P...
    for /f "tokens=5" %%A in ('netstat -ano ^| findstr :%%P ^| findstr LISTENING') do (
        echo Killing PID %%A on port %%P
        taskkill /PID %%A /F
    )
)

echo.
echo Current status:
netstat -ano | findstr :8765
netstat -ano | findstr :8766
echo.
echo Done.
pause
