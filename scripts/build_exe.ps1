<#
PowerShell build script for AI Automation Suite

Builds using the project spec file to include PyQt5 runtime and resources properly.
It prefers the project venv if present.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve project root from this script's location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir '..')
Set-Location $ProjectRoot

# Pick Python: prefer .venv
$VenvPython = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (Test-Path $VenvPython) {
    $python = $VenvPython
} else {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) {
        $python = $cmd.Source
    } else {
        throw 'Python not found. Please install Python or create a .venv.'
    }
}

# Ensure dependencies
& $python -m pip install --upgrade pip
if (Test-Path 'requirements.txt') {
    & $python -m pip install -r requirements.txt
} else {
    & $python -m pip install "pyinstaller>=6.1,<7" "pyinstaller-hooks-contrib>=2024.8"
}

# Clean and build with spec (tolerate locks)
if (Test-Path 'build') {
    try { Remove-Item -Recurse -Force 'build' } catch { 
        $bk = "build_old_" + (Get-Date -Format yyyyMMdd_HHmmss)
        Rename-Item 'build' $bk -ErrorAction SilentlyContinue
    }
}
if (Test-Path 'dist')  {
    try { Remove-Item -Recurse -Force 'dist' } catch { 
        $bk = "dist_old_" + (Get-Date -Format yyyyMMdd_HHmmss)
        Rename-Item 'dist' $bk -ErrorAction SilentlyContinue
    }
}

& $python -m PyInstaller --clean --noconfirm pyinstaller.spec

$exePath = Join-Path $ProjectRoot 'dist\AI_Automation_Suite\AI_Automation_Suite.exe'
if (Test-Path $exePath) {
    Write-Host "Executable created successfully:" -ForegroundColor Green
    Write-Host $exePath
    exit 0
} else {
    Write-Host "Failed to create executable." -ForegroundColor Red
    exit 1
}