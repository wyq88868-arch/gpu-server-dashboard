@echo off
setlocal
cd /d "%~dp0"
title Build GPU Server Dashboard V2.4 - Clean Conda Environment

echo ============================================================
echo GPU Server Dashboard V2.4 - Clean EXE Build
echo ============================================================
echo This script creates an isolated Conda environment:
echo gpu-dashboard-build
echo.
echo It will NOT modify your current base environment.
echo.
echo Output:
echo %CD%\dist\GPU-Server-Dashboard.exe
echo.
echo Log:
echo %CD%\build_clean_log.txt
echo ============================================================
echo.

echo [%date% %time%] Build started > build_clean_log.txt

where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: conda command was not found.
    echo ERROR: conda command was not found. >> build_clean_log.txt
    echo.
    echo Please open "Anaconda Prompt" and run this BAT there.
    echo Or add Anaconda to PATH.
    pause
    exit /b 1
)

echo Checking build environment...
conda env list | findstr /R /C:"^gpu-dashboard-build " >nul 2>nul

if %errorlevel% neq 0 (
    echo Creating clean Conda environment...
    conda create -n gpu-dashboard-build python=3.12 -y >> build_clean_log.txt 2>&1

    if %errorlevel% neq 0 (
        echo Failed to create Conda environment.
        type build_clean_log.txt
        pause
        exit /b 1
    )
) else (
    echo Existing environment found: gpu-dashboard-build
)

echo.
echo Installing dependencies in isolated environment...
conda run -n gpu-dashboard-build python -m pip install --upgrade pip >> build_clean_log.txt 2>&1
conda run -n gpu-dashboard-build python -m pip install pywebview pyinstaller >> build_clean_log.txt 2>&1

if %errorlevel% neq 0 (
    echo Dependency installation failed.
    type build_clean_log.txt
    pause
    exit /b 1
)

echo.
echo Removing old build output...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GPU-Server-Dashboard.spec del /q GPU-Server-Dashboard.spec

echo.
echo Building EXE without console...
conda run -n gpu-dashboard-build python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "GPU-Server-Dashboard" ^
  --icon "app.ico" ^
  gpu_server_dashboard_v24.py >> build_clean_log.txt 2>&1

if %errorlevel%==0 (
    echo.
    echo ============================================================
    echo Build succeeded.
    echo EXE:
    echo %CD%\dist\GPU-Server-Dashboard.exe
    echo ============================================================
    echo SUCCESS >> build_clean_log.txt
) else (
    echo.
    echo ============================================================
    echo Build failed.
    echo See build_clean_log.txt
    echo ============================================================
    echo FAILED >> build_clean_log.txt
)

echo.
echo ---- build_clean_log.txt ----
type build_clean_log.txt
echo -----------------------------
echo.
pause
