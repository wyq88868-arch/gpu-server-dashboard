@echo off
setlocal
cd /d "%~dp0"
title Build GPU Server Dashboard V2.4 Debug Console

set PY3=
where py >nul 2>nul
if %errorlevel%==0 set PY3=py -3
if "%PY3%"=="" set PY3=python

%PY3% -m pip install -r requirements.txt
%PY3% -m PyInstaller --noconfirm --clean --onefile --console --name "GPU-Server-Dashboard-Debug" --icon "app.ico" gpu_server_dashboard_v24.py

pause
