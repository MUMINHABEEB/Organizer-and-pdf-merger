#!/usr/bin/env powershell
# AI Automation Suite - Release Build Script
# This script automates the entire release process

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$false)]
    [string]$ReleaseNotes = "Bug fixes and improvements"
)

Write-Host "=== AI Automation Suite Release Builder ===" -ForegroundColor Green
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host "Release Notes: $ReleaseNotes" -ForegroundColor Yellow

# 1. Update version in files
Write-Host "`n1. Updating version numbers..." -ForegroundColor Cyan

# Update pyproject.toml
(Get-Content "pyproject.toml") -replace 'version = ".*"', "version = `"$Version`"" | Set-Content "pyproject.toml"

# Update version.py
(Get-Content "src\version.py") -replace '__version__ = ".*"', "__version__ = `"$Version`"" | Set-Content "src\version.py"

# Update installer script
(Get-Content "INSTALLER_InnoSetup.iss") -replace '#define MyAppVersion ".*"', "#define MyAppVersion `"$Version`"" | Set-Content "INSTALLER_InnoSetup.iss"

Write-Host "✓ Version numbers updated" -ForegroundColor Green

# 2. Build frontend
Write-Host "`n2. Building frontend..." -ForegroundColor Cyan
scripts\build_frontend.ps1 -Production
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Frontend built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend build failed" -ForegroundColor Red
    exit 1
}

# 3. Build executables
Write-Host "`n3. Building executables..." -ForegroundColor Cyan
scripts\build_exe.ps1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Standard executable built" -ForegroundColor Green
} else {
    Write-Host "✗ Standard executable build failed" -ForegroundColor Red
    exit 1
}

scripts\build_onefile_exe.ps1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Onefile executable built" -ForegroundColor Green
} else {
    Write-Host "✗ Onefile executable build failed" -ForegroundColor Red
    exit 1
}

# 4. Build installer
Write-Host "`n4. Building installer..." -ForegroundColor Cyan
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "INSTALLER_InnoSetup.iss"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Installer built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Installer build failed" -ForegroundColor Red
    exit 1
}

# 5. Create release package
Write-Host "`n5. Creating release package..." -ForegroundColor Cyan
$releaseDir = "releases\v$Version"
New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null

# Copy files to release directory
Copy-Item "installer_output\AI_Automation_Suite_Setup.exe" "$releaseDir\AI_Automation_Suite_Setup_v$Version.exe"
Copy-Item "dist\AI_Automation_Suite_OneFile\AI_Automation_Suite_OneFile.exe" "$releaseDir\AI_Automation_Suite_v$Version.exe"

# Create release notes
@"
# AI Automation Suite v$Version

## Release Notes
$ReleaseNotes

## Installation Options

### Professional Installer (Recommended)
- **File**: AI_Automation_Suite_Setup_v$Version.exe
- **Size**: ~83 MB
- **Features**: Full Windows integration, Start Menu shortcuts, automatic WebView2 installation

### Portable Version
- **File**: AI_Automation_Suite_v$Version.exe  
- **Size**: ~6 MB
- **Features**: Single-file, no installation required
- **Requirement**: WebView2 Runtime (install once: ``winget install Microsoft.EdgeWebView2Runtime``)

## What's New
- $ReleaseNotes

## System Requirements
- Windows 10/11
- WebView2 Runtime (auto-installed with professional installer)

---
*Built on $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")*
"@ | Out-File "$releaseDir\README.md" -Encoding UTF8

Write-Host "✓ Release package created in: $releaseDir" -ForegroundColor Green

# 6. Generate checksums
Write-Host "`n6. Generating checksums..." -ForegroundColor Cyan
Get-ChildItem "$releaseDir\*.exe" | ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    "$($hash.Hash.ToLower())  $($_.Name)" | Out-File "$releaseDir\checksums.txt" -Append -Encoding UTF8
}
Write-Host "✓ Checksums generated" -ForegroundColor Green

Write-Host "`n=== Release v$Version Complete! ===" -ForegroundColor Green
Write-Host "Release files available in: $releaseDir" -ForegroundColor Yellow
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "1. Test the release files" -ForegroundColor Gray
Write-Host "2. Upload to your distribution server/GitHub" -ForegroundColor Gray
Write-Host "3. Update version check endpoint" -ForegroundColor Gray
Write-Host "4. Announce the release" -ForegroundColor Gray
