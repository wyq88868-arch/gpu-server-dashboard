@echo off
setlocal
cd /d "%~dp0"
title Install Dependencies - Python3 Only - TUNA Mirror

echo ============================================================
echo Server Resource Dashboard - Dependency Installer
echo Python3 Only + TUNA Mirror
echo ============================================================
echo Log file:
echo %CD%\install_log_tuna.txt
echo.

echo [%date% %time%] Start install with TUNA mirror > install_log_tuna.txt
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
    echo ERROR: Python 3 was not found. >> install_log_tuna.txt
    echo Please install Python 3 first:
    echo https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

echo Using Python 3 command: %PY3%
echo Using Python 3 command: %PY3% >> install_log_tuna.txt
%PY3% --version
%PY3% --version >> install_log_tuna.txt 2>&1

echo.
echo Installing with TUNA mirror...
%PY3% -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple >> install_log_tuna.txt 2>&1
%PY3% -m pip install pywebview -i https://pypi.tuna.tsinghua.edu.cn/simple >> install_log_tuna.txt 2>&1

if %errorlevel%==0 (
    echo.
    echo SUCCESS.
    echo Now run run_desktop_app.bat
    echo SUCCESS >> install_log_tuna.txt
) else (
    echo.
    echo FAILED. Please send install_log_tuna.txt to ChatGPT.
    echo FAILED >> install_log_tuna.txt
)

echo.
echo ---- install_log_tuna.txt ----
type install_log_tuna.txt
echo ------------------------------
echo.
pause
