@echo off
cd /d "%~dp0"
echo ========================================================
echo Relu Consultancy Hiring Challenge - GitHub Host Script
echo ========================================================
powershell -ExecutionPolicy Bypass -File "%~dp0push_to_github.ps1"
pause
