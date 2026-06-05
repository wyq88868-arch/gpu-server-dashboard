@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title GPU Server Dashboard V2.4 - Clean Conda Build FIXED

echo ============================================================
echo GPU Server Dashboard V2.4 - Clean EXE Build FIXED
echo ============================================================
echo Fix: all Conda BAT calls now use CALL.
echo Environment: gpu-dashboard-build
echo Output: %CD%\dist\GPU-Server-Dashboard.exe
echo Log: %CD%\build_clean_log.txt
echo ============================================================
echo.

echo [%date% %time%] Build started > build_clean_log.txt

where conda >nul 2>nul
if errorlevel 1 (
    echo ERROR: conda was not found.
    echo ERROR: conda was not found. >> build_clean_log.txt
    echo.
    echo Open Anaconda Prompt and run this BAT from there.
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Conda...
call conda --version
if errorlevel 1 (
    echo ERROR: conda command failed.
    echo ERROR: conda command failed. >> build_clean_log.txt
    pause
    exit /b 1
)
call conda --version >> build_clean_log.txt 2>&1

echo.
echo [2/5] Checking build environment...
call conda env list | findstr /R /C:"^gpu-dashboard-build " >nul 2>nul

if errorlevel 1 (
    echo Creating environment gpu-dashboard-build...
    call conda create -n gpu-dashboard-build python=3.12 -y >> build_clean_log.txt 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to create environment.
        echo.
        type build_clean_log.txt
        pause
        exit /b 1
    )
) else (
    echo Existing environment found: gpu-dashboard-build
)

echo.
echo [3/5] Installing pip, pywebview and PyInstaller...
echo This may take several minutes.

call conda run -n gpu-dashboard-build python -m pip install --upgrade pip >> build_clean_log.txt 2>&1
if errorlevel 1 (
    echo ERROR: pip upgrade failed.
    echo.
    type build_clean_log.txt
    pause
    exit /b 1
)

call conda run -n gpu-dashboard-build python -m pip install pywebview pyinstaller >> build_clean_log.txt 2>&1
if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    echo.
    type build_clean_log.txt
    pause
    exit /b 1
)

echo.
echo [4/5] Cleaning old build output...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GPU-Server-Dashboard.spec del /q GPU-Server-Dashboard.spec

echo.
echo [5/5] Building EXE without console...
call conda run -n gpu-dashboard-build python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "GPU-Server-Dashboard" ^
  --icon "app.ico" ^
  gpu_server_dashboard_v24.py >> build_clean_log.txt 2>&1

if errorlevel 1 (
    echo.
    echo ============================================================
    echo BUILD FAILED
    echo See build_clean_log.txt below.
    echo ============================================================
    echo FAILED >> build_clean_log.txt
    echo.
    type build_clean_log.txt
    pause
    exit /b 1
)

echo.
echo ============================================================
echo BUILD SUCCEEDED
echo EXE:
echo %CD%\dist\GPU-Server-Dashboard.exe
echo ============================================================
echo SUCCESS >> build_clean_log.txt
echo.
pause
