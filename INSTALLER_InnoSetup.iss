; Inno Setup script for AI Automation Suite
; Build with Inno Setup Compiler after generating dist folder.

#define MyAppName "AI Automation Suite"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Ramidos"
#define MyAppExe "AI_Automation_Suite_Web.exe"
#define MyAppDir "dist\\AI_Automation_Suite"

[Setup]
AppId={{3E8E8F4A-7D25-4B4F-9A21-9D9F4D4B1234}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\\{#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=AI_Automation_Suite_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\\{#MyAppExe}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "{#MyAppDir}\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExe}"; WorkingDir: "{app}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExe}"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\\{#MyAppExe}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
