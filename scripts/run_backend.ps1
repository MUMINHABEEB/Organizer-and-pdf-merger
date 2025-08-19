param(
    [int]$Port = 8000
)

# Activates virtual environment if present
if (Test-Path .venv/Scripts/Activate.ps1) { . .venv/Scripts/Activate.ps1 }

Write-Host "Starting FastAPI backend on port $Port..."
uvicorn backend.server:app --host 127.0.0.1 --port $Port --reload
