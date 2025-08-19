param(
    [switch]$Production
)

$ErrorActionPreference = 'Stop'

Write-Host '--- Building frontend (Vite) ---'

Push-Location "$PSScriptRoot/../frontend"
try {
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        throw 'npm is not installed or not in PATH.'
    }

    if (-not (Test-Path node_modules)) {
        Write-Host 'Installing npm dependencies...'
        npm install --no-audit --no-fund
    }

    if ($Production) {
        Write-Host 'Running production build (vite build)...'
        npx vite build
    }
    else {
        Write-Host 'Running development build (vite build)...'
        npx vite build
    }

    Write-Host 'Frontend build complete.'
}
finally {
    Pop-Location
}
