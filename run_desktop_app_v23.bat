@echo off
setlocal
cd /d "%~dp0"
title Server Resource Dashboard V2.3 - Port 8766

echo ============================================================
echo Starting Server Resource Dashboard V2.3...
echo Fixes:
echo 1. Real incremental DOM updates for smooth scrolling
echo 2. CPU process table redesigned
echo 3. Core CPU percent and total CPU percent separated
echo.
echo Backend: SSH remote python3
echo Local port: 8766
echo Log file:
echo %CD%\run_log_v23.txt
echo ============================================================
echo.

echo [%date% %time%] Start app V2.3 > run_log_v23.txt
set PY3=

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 --version >nul 2>nul
    if %errorlevel%==0 (
        set PY3=py -3
    )
)

if "%PY3%"=="" (
    where python3 >nul 2>nul
    if %errorlevel%==0 (
        python3 --version >nul 2>nul
        if %errorlevel%==0 (
            set PY3=python3
        )
    )
)

if "%PY3%"=="" (
    echo ERROR: Python 3 was not found.
    echo ERROR: Python 3 was not found. >> run_log_v23.txt
    echo Please install Python 3 first.
    pause
    exit /b 1
)

echo Using Python 3 command: %PY3%
echo Using Python 3 command: %PY3% >> run_log_v23.txt

%PY3% beautiful_server_dashboard_desktop_v23.py >> run_log_v23.txt 2>&1

echo.
echo App exited or failed.
echo ---- run_log_v23.txt ----
type run_log_v23.txt
echo -------------------------
echo.
pause
