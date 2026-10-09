#define Ver GetEnv("APP_VERSION")
[Setup]
AppName=AI Anti-Duplicate
AppVersion={#Ver}
AppPublisher=Nikolay Fedotov
AppPublisherURL=https://tech-crm.ru/
DefaultDirName={autopf}\AI Anti-Duplicate
DefaultGroupName=AI Anti-Duplicate
OutputDir=..\release
OutputBaseFilename=AI-Anti-Duplicate-{#Ver}-Setup
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\AI-Anti-Duplicate.exe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
[Files]
Source: "..\dist\AI-Anti-Duplicate\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
[Icons]
Name: "{group}\AI Anti-Duplicate"; Filename: "{app}\AI-Anti-Duplicate.exe"
Name: "{autodesktop}\AI Anti-Duplicate"; Filename: "{app}\AI-Anti-Duplicate.exe"
[Run]
Filename: "{app}\AI-Anti-Duplicate.exe"; Description: "Запустить"; Flags: nowait postinstall skipifsilent
