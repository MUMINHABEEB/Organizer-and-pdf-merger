# Frontend (React + Vite)

Prototype web UI for AI Automation Suite.

## Dev Quick Start

1. Install Node.js (already detected v22 on your machine).
2. In PowerShell:
```
cd frontend
npm install
npm run dev
```
3. Backend must be running (PowerShell at project root):
```
powershell -ExecutionPolicy Bypass -File scripts/run_backend.ps1
```
4. Open the printed localhost URL (default: http://127.0.0.1:5173).

## Panels
- Organizer: Calls POST /organize.
- PDF Merge: Uploads PDFs to /merge_pdfs.

This is an early scaffold; styling and routing will be improved later.
