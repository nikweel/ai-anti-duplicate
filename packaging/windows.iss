#define Ver GetEnv("APP_VERSION")
[Setup]
AppName=Photo Duplicate Finder AI
AppVersion={#Ver}
AppPublisher=Nikolay Fedotov
AppPublisherURL=https://tech-crm.ru/
DefaultDirName={autopf}\Photo Duplicate Finder AI
DefaultGroupName=Photo Duplicate Finder AI
OutputDir=..\release
OutputBaseFilename=Photo-Duplicate-Finder-AI-{#Ver}-Setup
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\Photo-Duplicate-Finder-AI.exe
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
[Files]
Source: "..\dist\Photo-Duplicate-Finder-AI\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
[Icons]
Name: "{group}\Photo Duplicate Finder AI"; Filename: "{app}\Photo-Duplicate-Finder-AI.exe"
Name: "{autodesktop}\Photo Duplicate Finder AI"; Filename: "{app}\Photo-Duplicate-Finder-AI.exe"
[Run]
Filename: "{app}\Photo-Duplicate-Finder-AI.exe"; Description: "Запустить"; Flags: nowait postinstall skipifsilent
