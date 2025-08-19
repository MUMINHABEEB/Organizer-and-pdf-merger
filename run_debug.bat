@echo off
echo Starting AI Automation Suite...
cd /d "%~dp0dist\AI_Automation_Suite"
AI_Automation_Suite_Web.exe
echo.
echo Exit code: %ERRORLEVEL%
pause
