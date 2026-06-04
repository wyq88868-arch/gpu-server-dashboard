@echo off
setlocal
cd /d "%~dp0"
title Test Remote Server Python3

echo ============================================================
echo Testing remote server python3 and nvidia-smi
echo ============================================================
echo.
set HOST=wyqserver
if not "%1"=="" set HOST=%1

echo Host: %HOST%
echo.
echo [1] ssh %HOST% python3 --version
ssh %HOST% python3 --version
echo.
echo [2] ssh %HOST% "which python3; which nvidia-smi; nvidia-smi -L"
ssh %HOST% "which python3; which nvidia-smi; nvidia-smi -L"
echo.
pause
