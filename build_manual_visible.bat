@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title GPU Dashboard Manual Build Debug

echo Running each step visibly.
echo.

echo STEP 1: Conda version
call conda --version
if errorlevel 1 goto :fail

echo.
echo STEP 2: Python in build environment
call conda run -n gpu-dashboard-build python --version
if errorlevel 1 goto :fail

echo.
echo STEP 3: Install dependencies
call conda run -n gpu-dashboard-build python -m pip install pywebview pyinstaller
if errorlevel 1 goto :fail

echo.
echo STEP 4: Build
call conda run -n gpu-dashboard-build python -m PyInstaller --noconfirm --clean --onefile --windowed --name "GPU-Server-Dashboard" --icon "app.ico" gpu_server_dashboard_v24.py
if errorlevel 1 goto :fail

echo.
echo SUCCESS: dist\GPU-Server-Dashboard.exe
pause
exit /b 0

:fail
echo.
echo FAILED at the step shown above.
pause
exit /b 1
