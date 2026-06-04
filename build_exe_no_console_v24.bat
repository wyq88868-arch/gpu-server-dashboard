@echo off
setlocal
cd /d "%~dp0"
title Build GPU Server Dashboard V2.4 EXE - No Console

echo ============================================================
echo Build GPU Server Dashboard V2.4 EXE
echo Fix: hide ssh.exe child console popup
echo Output:
echo dist\GPU-Server-Dashboard.exe
echo Log:
echo %CD%\build_log.txt
echo ============================================================
echo.

echo [%date% %time%] Build started > build_log.txt

set PY3=
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 --version >nul 2>nul
    if %errorlevel%==0 set PY3=py -3
)

if "%PY3%"=="" (
    where python3 >nul 2>nul
    if %errorlevel%==0 (
        python3 --version >nul 2>nul
        if %errorlevel%==0 set PY3=python3
    )
)

if "%PY3%"=="" (
    echo ERROR: Python 3 was not found.
    echo ERROR: Python 3 was not found. >> build_log.txt
    pause
    exit /b 1
)

echo Using Python 3 command: %PY3%
echo Using Python 3 command: %PY3% >> build_log.txt

echo Installing dependencies...
%PY3% -m pip install --upgrade pip >> build_log.txt 2>&1
%PY3% -m pip install -r requirements.txt >> build_log.txt 2>&1

if %errorlevel% neq 0 (
    echo Dependency installation failed. See build_log.txt.
    type build_log.txt
    pause
    exit /b 1
)

echo Building no-console EXE...
%PY3% -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "GPU-Server-Dashboard" ^
  --icon "app.ico" ^
  gpu_server_dashboard_v24.py >> build_log.txt 2>&1

if %errorlevel%==0 (
    echo.
    echo ============================================================
    echo Build succeeded.
    echo EXE:
    echo %CD%\dist\GPU-Server-Dashboard.exe
    echo ============================================================
    echo SUCCESS >> build_log.txt
) else (
    echo.
    echo Build failed. See build_log.txt.
    echo FAILED >> build_log.txt
)

echo.
type build_log.txt
echo.
pause
