@echo off
setlocal
cd /d "%~dp0"
title Install Dependencies - Python3 Only

echo ============================================================
echo Server Resource Dashboard - Dependency Installer
echo ============================================================
echo This script requires Python 3.
echo It will NOT use Python 2.
echo.
echo Log file:
echo %CD%\install_log.txt
echo ============================================================
echo.

echo [%date% %time%] Start install > install_log.txt
echo Current directory: %CD% >> install_log.txt

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
    echo ERROR: Python 3 was not found. >> install_log.txt
    echo.
    echo Your current python may be Python 2.7. Do NOT use it for this app.
    echo Please install Python 3 first and check "Add Python to PATH".
    echo Download:
    echo https://www.python.org/downloads/windows/
    echo.
    echo After installing Python 3, run this file again.
    echo.
    pause
    exit /b 1
)

echo Using Python 3 command: %PY3%
echo Using Python 3 command: %PY3% >> install_log.txt

%PY3% --version
%PY3% --version >> install_log.txt 2>&1

echo.
echo Upgrading pip...
%PY3% -m pip install --upgrade pip >> install_log.txt 2>&1

echo.
echo Installing pywebview...
%PY3% -m pip install pywebview >> install_log.txt 2>&1

if %errorlevel%==0 (
    echo.
    echo ============================================================
    echo SUCCESS.
    echo Now run:
    echo run_desktop_app.bat
    echo ============================================================
    echo SUCCESS >> install_log.txt
) else (
    echo.
    echo ============================================================
    echo FAILED.
    echo Please send install_log.txt to ChatGPT.
    echo ============================================================
    echo FAILED >> install_log.txt
)

echo.
echo ---- install_log.txt ----
type install_log.txt
echo -------------------------
echo.
pause
