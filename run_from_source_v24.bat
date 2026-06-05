@echo off
setlocal
cd /d "%~dp0"
title Run GPU Server Dashboard V2.4 from Source

set PY3=
where py >nul 2>nul
if %errorlevel%==0 set PY3=py -3
if "%PY3%"=="" set PY3=python

%PY3% -m pip install pywebview
%PY3% gpu_server_dashboard_v24.py

pause
