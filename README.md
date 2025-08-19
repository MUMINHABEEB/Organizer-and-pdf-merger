# AI Automation Suite - Organizer and PDF Merger

A comprehensive automation toolkit for file organization, PDF management, and intelligent file naming with modern web-based interface.

## 🎯 Features

- **Smart File Organization**: Automatically organize files by date, type, and content
- **PDF Tools**: Merge, split, and organize PDF documents
- **Calendar Integration**: Sort files by calendar events and dates
- **AI-Powered Naming**: Intelligent file naming suggestions
- **Modern UI**: Clean, responsive web-based interface
- **Ramidos Branding**: Professional company theme

## � Installation Guide

### Option 1: Professional Installer (Recommended for End Users)

1. **Download the Installer**
   - Go to [Releases](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/releases)
   - Download the latest `AI_Automation_Suite_Setup.exe` (83MB)

2. **Install the Application**
   - Run `AI_Automation_Suite_Setup.exe` as Administrator
   - Follow the installation wizard
   - WebView2 runtime will be installed automatically
   - Application will be added to Start Menu and Desktop

3. **Launch the Application**
   - Click on the desktop shortcut, or
   - Search "AI Automation Suite" in Start Menu

### Option 2: Portable Version (For IT/Advanced Users)

1. **Download Portable Executable**
   - Go to [Releases](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/releases)
   - Download `AI_Automation_Suite_OneFile.exe` (6MB)

2. **Install WebView2 Runtime** (Required)
   ```powershell
   winget install Microsoft.EdgeWebView2Runtime
   ```
   Or download from [Microsoft WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)

3. **Run the Application**
   - Double-click `AI_Automation_Suite_OneFile.exe`
   - No installation required - fully portable

### Option 3: Developer Version

1. **Download Standard Executable**
   - Go to [Releases](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/releases)
   - Download `AI_Automation_Suite.exe` + folder

2. **Extract and Run**
   - Extract all files to a folder
   - Ensure WebView2 is installed (see Option 2)
   - Run `AI_Automation_Suite.exe`

## �️ System Requirements

- **Operating System**: Windows 10 (version 1909 or later) or Windows 11
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB free disk space
- **Runtime**: WebView2 (auto-installed with professional installer)
- **Permissions**: Administrator rights for installation (Option 1 only)

## 🚀 Quick Start Guide

### Using File Organizer
1. Launch the application
2. Click "File Organizer" tab
3. Select source folder to organize
4. Choose organization scheme (by date, type, etc.)
5. Preview changes (dry run mode)
6. Apply organization

### Using PDF Merger
1. Click "PDF Tools" tab
2. Select "Merge PDFs" option
3. Add PDF files using "Browse" or drag-and-drop
4. Arrange files in desired order
5. Click "Merge" and choose output location

### Using Smart File Naming
1. Click "File Naming" tab
2. Select files to rename
3. Choose naming pattern or use AI suggestions
4. Preview new names
5. Apply changes

## 🔄 Updates

The application automatically checks for updates and will notify you when new versions are available. You can also manually check for updates in the Help menu.

## 🛠️ Development

### Building from Source

1. **Setup Environment:**
   ```powershell
   git clone https://github.com/MUMINHABEEB/Organizer-and-pdf-merger
   cd Organizer-and-pdf-merger
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
Organizer-and-pdf-merger/
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

## 📋 Troubleshooting

### Common Issues

**Application won't start:**
- Ensure WebView2 is installed: `winget install Microsoft.EdgeWebView2Runtime`
- Run as Administrator if using portable version
- Check Windows version compatibility (Windows 10 1909+ required)

**PDF Merge fails:**
- Ensure PDF files are not password-protected
- Check available disk space
- Verify PDF files are not corrupted

**File Organization not working:**
- Check folder permissions
- Ensure source folder exists and is accessible
- Try running as Administrator

**Windows Defender warnings:**
- Add application to Windows Defender exclusions
- Verify SHA256 checksums from release page
- Download only from official GitHub releases

### Getting Help

1. Check the [Issues](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/issues) page
2. Create a new issue with:
   - Windows version
   - Application version
   - Steps to reproduce
   - Error messages (if any)

## 🔐 Security & Privacy

- **No Data Collection**: The application doesn't collect or transmit personal data
- **Local Processing**: All file operations are performed locally on your machine
- **Open Source**: Full source code available for security review
- **Digital Signatures**: Future releases will include code signing certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🏢 About Ramidos

AI Automation Suite is developed by Ramidos, specializing in intelligent automation solutions for modern productivity needs.

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/issues)
- **Documentation**: Check this README and release notes
- **Community**: Join discussions in the repository

---

## 📥 Download Links

**Latest Release:** [Download from GitHub Releases](https://github.com/MUMINHABEEB/Organizer-and-pdf-merger/releases/latest)

- **🏢 Professional Installer** (`AI_Automation_Suite_Setup.exe`) - Recommended for most users
- **📱 Portable Version** (`AI_Automation_Suite_OneFile.exe`) - For technical users and IT deployment
- **🔧 Developer Version** (`AI_Automation_Suite.exe`) - For development and testing

**Repository:** https://github.com/MUMINHABEEB/Organizer-and-pdf-merger