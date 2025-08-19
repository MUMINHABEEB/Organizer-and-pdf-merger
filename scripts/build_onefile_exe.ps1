<#
Build single-file (onefile) PyInstaller executable.
Produces dist/AI_Automation_Suite_OneFile/AI_Automation_Suite_OneFile.exe
#>
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir '..')
Set-Location $ProjectRoot

$VenvPython = Join-Path $ProjectRoot '.venv/\Scripts/python.exe'
if(Test-Path $VenvPython){ $python = $VenvPython } else { $python = (Get-Command python).Source }

Write-Host '== Ensuring dependencies =='
& $python -m pip install --upgrade pip | Out-Null
& $python -m pip install "pyinstaller>=6.1,<7" "pyinstaller-hooks-contrib>=2024.8" | Out-Null

Write-Host '== Building frontend (production) =='
& powershell -ExecutionPolicy Bypass -File "$ProjectRoot/scripts/build_frontend.ps1" -Production

Write-Host '== Building onefile executable =='
& $python -m PyInstaller --clean --noconfirm pyinstaller_onefile.spec

$exe = Join-Path $ProjectRoot 'dist/AI_Automation_Suite_OneFile/AI_Automation_Suite_OneFile.exe'
if(Test-Path $exe){
  Write-Host "Onefile EXE ready: $exe" -ForegroundColor Green
} else {
  Write-Host 'Build failed.' -ForegroundColor Red
  exit 1
}
