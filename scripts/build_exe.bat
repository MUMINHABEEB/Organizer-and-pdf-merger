@echo off
setlocal
set "ROOT=%~dp0.."
set "PY=%ROOT%\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
pushd "%ROOT%"
"%PY%" -m pip install --upgrade "pyinstaller>=6.1,<7" "pyinstaller-hooks-contrib>=2024.8"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
"%PY%" -m PyInstaller --clean --noconfirm pyinstaller.spec
popd
if exist "%ROOT%\dist\AI_Automation_Suite\AI_Automation_Suite.exe" (
  echo Built: %ROOT%\dist\AI_Automation_Suite\AI_Automation_Suite.exe
) else (
  echo Build failed.
  exit /b 1
)