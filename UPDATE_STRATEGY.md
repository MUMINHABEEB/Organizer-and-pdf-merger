# AI Automation Suite - Update Distribution Guide

## 🚀 Update Distribution Strategies

### **Option 1: GitHub Releases (Recommended - Free)**
1. **Setup:**
   - Create GitHub repository
   - Use GitHub Actions for automated builds
   - Release assets auto-distributed via CDN

2. **Workflow:**
   ```bash
   # Tag new version
   git tag v1.0.1
   git push origin v1.0.1
   
   # GitHub Actions automatically:
   # - Builds executables
   # - Creates installer
   # - Publishes release
   ```

3. **Update API endpoint:**
   ```
   https://api.github.com/repos/yourusername/ai-automation-suite/releases/latest
   ```

### **Option 2: Simple Web Server**
1. **Setup:**
   - Upload files to web server
   - Create simple API endpoint
   - Host version.json file

2. **File structure:**
   ```
   your-website.com/
   ├── downloads/
   │   ├── v1.0.1/
   │   │   ├── AI_Automation_Suite_Setup_v1.0.1.exe
   │   │   └── AI_Automation_Suite_v1.0.1.exe
   │   └── latest/
   │       ├── AI_Automation_Suite_Setup.exe
   │       └── AI_Automation_Suite.exe
   └── api/
       └── version.json
   ```

3. **version.json example:**
   ```json
   {
     "latest_version": "1.0.1",
     "download_url": "https://your-website.com/downloads/latest/",
     "release_notes": "Bug fixes and performance improvements",
     "release_date": "2025-08-19",
     "minimum_version": "1.0.0"
   }
   ```

### **Option 3: Enterprise Distribution**
1. **Internal network deployment**
2. **Group Policy software installation**
3. **SCCM/Intune management**

## 📋 Update Process Workflow

### **For Major Updates (1.0.0 → 2.0.0):**
1. **Development:**
   ```powershell
   # Build and test
   scripts\build_release.ps1 -Version "2.0.0" -ReleaseNotes "Major new features"
   ```

2. **Distribution:**
   ```powershell
   # Upload to server/GitHub
   # Update version endpoint
   # Notify users
   ```

### **For Minor Updates (1.0.0 → 1.0.1):**
1. **Quick fixes:**
   ```powershell
   scripts\build_release.ps1 -Version "1.0.1" -ReleaseNotes "Bug fixes"
   ```

2. **Silent deployment** (optional)

### **For Patches (1.0.1 → 1.0.2):**
1. **Security/critical fixes**
2. **Automatic notification recommended**

## 🔧 Integration with Your App

### **Add to webview_bootstrap.py:**
```python
from src.updater import UpdateChecker

# In main() function or API class:
def check_updates():
    updater = UpdateChecker()
    updater.check_for_updates(silent=False)
    return updater.get_update_info()
```

### **Add to frontend UI:**
```javascript
// Check for updates periodically
setInterval(async () => {
    const updateInfo = await pywebview.api.check_updates();
    if (updateInfo.update_available) {
        showUpdateNotification(updateInfo);
    }
}, 24 * 60 * 60 * 1000); // Check daily
```

## 📦 Deployment Automation

### **GitHub Actions Workflow (.github/workflows/release.yml):**
```yaml
name: Build and Release
on:
  push:
    tags: ['v*']
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build Release
        run: scripts\build_release.ps1 -Version ${{ github.ref_name }}
      - name: Create Release
        uses: actions/create-release@v1
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          files: releases/**/*
```

## 🎯 Best Practices

### **Version Numbering:**
- **Major.Minor.Patch** (e.g., 1.2.3)
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### **Release Notes:**
- Clear, user-friendly language
- List new features and fixes
- Mention any breaking changes

### **Testing:**
- Test installer on clean Windows machines
- Verify auto-update mechanism
- Check backward compatibility

### **Communication:**
- Email notifications for major updates
- In-app notifications for minor updates
- Documentation updates

## 🔄 Example Release Command

```powershell
# For next update:
cd "D:\Programming\AI Automation Files\AI Automation Files made by AI\ai-automation-suite"
scripts\build_release.ps1 -Version "1.0.1" -ReleaseNotes "Fixed file organization bug and improved PDF merging"
```

This creates everything you need for distribution!
