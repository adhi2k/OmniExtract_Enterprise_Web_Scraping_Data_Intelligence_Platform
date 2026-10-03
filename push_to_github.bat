@echo off
cd /d "%~dp0"
echo ========================================================
echo OmniExtract Platform - GitHub Deployment Launcher
echo ========================================================
powershell -ExecutionPolicy Bypass -File "%~dp0push_to_github.ps1"
pause
