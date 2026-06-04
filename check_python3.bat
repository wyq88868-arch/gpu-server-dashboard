@echo off
setlocal
cd /d "%~dp0"
title Check Python Environment

echo ============================================================
echo Python environment check
echo ============================================================
echo.

echo [where py]
where py
echo.

echo [py -0p]
py -0p
echo.

echo [py -3 --version]
py -3 --version
echo.

echo [where python]
where python
echo.

echo [python --version]
python --version
echo.

echo If python is Python 2.7, that is okay, but this app needs py -3.
echo If py -3 does not work, install Python 3 from:
echo https://www.python.org/downloads/windows/
echo.
pause
