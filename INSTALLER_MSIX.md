# MSIX Packaging (Manual Steps)

These are manual guidelines to create an MSIX package for AI Automation Suite.

1. Build the application (folder distribution):
   - PowerShell: `scripts/build_exe.ps1` (or onefile script if preferred).
   - Result: `dist/AI_Automation_Suite` directory with executables.

2. Prepare packaging layout (example using PowerShell):
   ```powershell
   $PackageRoot = "msix_layout"
   New-Item -ItemType Directory -Force -Path $PackageRoot\VFS\ProgramFiles\AI_Automation_Suite | Out-Null
   Copy-Item -Recurse dist/AI_Automation_Suite/* $PackageRoot/VFS/ProgramFiles/AI_Automation_Suite
   ```

3. Create `AppxManifest.xml` inside `$PackageRoot`:
   - Identity: Name="Ramidos.AIAutomationSuite" Publisher="CN=YourCompany" Version="0.1.0.0"
   - Set Executable entry point to `AI_Automation_Suite_Web.exe`.

4. Generate a self-signed certificate (development only):
   ```powershell
   $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=YourCompany" -CertStoreLocation Cert:\CurrentUser\My
   Export-PfxCertificate -Cert $cert -FilePath AIAutomationSuite.pfx -Password (ConvertTo-SecureString -String "Pass@123" -Force -AsPlainText)
   ```

5. Create MSIX package using MakeAppx:
   ```powershell
   makeappx pack /d msix_layout /p AI_Automation_Suite.msix
   ```

6. Sign the MSIX:
   ```powershell
   signtool sign /fd SHA256 /a /f .\AIAutomationSuite.pfx /p Pass@123 AI_Automation_Suite.msix
   ```

7. Install (developer mode enabled):
   - Double click the `.msix` file or run: `Add-AppxPackage AI_Automation_Suite.msix`

8. Updates: increment `Version` in the manifest and repeat pack + sign.

> NOTE: Full automation script can be added later if you choose MSIX as primary distribution. Inno Setup is simpler for broad Windows deployments without enabling Developer Mode.
