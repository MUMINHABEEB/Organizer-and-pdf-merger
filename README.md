# AI Automation Suite

A comprehensive automation toolkit for file organization, PDF management, and intelligent file naming.

## 🎯 Features

- **Smart File Organization**: Automatically organize files by date, type, and content
- **PDF Tools**: Merge, split, and organize PDF documents
- **Calendar Integration**: Sort files by calendar events and dates
- **AI-Powered Naming**: Intelligent file naming suggestions
- **Modern UI**: Clean, responsive web-based interface
- **Ramidos Branding**: Professional company theme

## 🚀 Quick Start

### Option 1: Professional Installer (Recommended)
1. Download the latest `AI_Automation_Suite_Setup.exe` from [Releases](../../releases)
2. Run the installer
3. Launch from Start Menu

### Option 2: Portable Version
1. Download `AI_Automation_Suite.exe` from [Releases](../../releases)
2. Install WebView2: `winget install Microsoft.EdgeWebView2Runtime`
3. Run the executable

## 📋 System Requirements

- Windows 10/11
- WebView2 Runtime (auto-installed with professional installer)
- 100MB free disk space

## 🔄 Updates

The application checks for updates automatically. You can also manually check for updates in the Help menu.

## 🛠️ Development

### Building from Source

1. **Setup Environment:**
   ```powershell
   git clone https://github.com/MUMINHABEEB/ai-automation-suite
   cd ai-automation-suite
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Build Frontend:**
   ```powershell
   scripts\build_frontend.ps1 -Production
   ```

3. **Build Executables:**
   ```powershell
   scripts\build_exe.ps1
   scripts\build_onefile_exe.ps1
   ```

4. **Create Release:**
   ```powershell
   scripts\build_release.ps1 -Version "1.0.1" -ReleaseNotes "Your changes"
   ```

### Project Structure
```
ai-automation-suite/
├── src/                    # Python backend
├── frontend/               # React frontend
├── scripts/                # Build scripts
├── dist/                   # Built executables
└── releases/               # Release packages
```

### Testing

Run automated tests to ensure functionality:

```powershell
pytest -q
```

View coverage report:
```powershell
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Backend API

The application uses a FastAPI backend with modern web UI:

```powershell
scripts\run_backend.ps1
# Visit http://127.0.0.1:8000/docs for API documentation
```

**Available Endpoints:**
- `GET /health` – Health check
- `POST /organize` – File organization
- `POST /merge_pdfs` – PDF merging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🏢 About Ramidos

AI Automation Suite is developed by Ramidos, specializing in intelligent automation solutions.

---

**Download the latest version from [Releases](../../releases)**