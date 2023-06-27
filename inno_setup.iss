#define MyAppName "My Program"
#define MyAppVersion "1.5"
#define MyAppPublisher "My Company, Inc."
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "MyProg.exe"
#define MyAppAssocName MyAppName + " File"
#define ExeSource "C:\Program Files (x86)\Inno Setup 6\Examples\MyProg.exe"

#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

#define MyAppAssocExt2 ".myp2"
#define MyAppAssocKey2 StringChange(MyAppAssocName, " ", "") + MyAppAssocExt2


[Setup]
AppId={{931B78F1-4C54-4E34-883F-1470C64243CB}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
OutputBaseFilename=mysetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#ExeSource}" ; DestDir: "{app}"; Flags: ignoreversion


[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids";             ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: "";                     Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}";                             ValueType: string; ValueName: "";                 ValueData: "{#MyAppAssocName}";    Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon";                 ValueType: string; ValueName: "";                 ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command";          ValueType: string; ValueName: "";                 ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes";  ValueType: string; ValueName: "{#MyAppAssocExt}";             ValueData: ""

Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt2}\OpenWithProgids";             ValueType: string; ValueName: "{#MyAppAssocKey2}"; ValueData: "";                     Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey2}";                             ValueType: string; ValueName: "";                 ValueData: "{#MyAppAssocName}";    Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey2}\DefaultIcon";                 ValueType: string; ValueName: "";                 ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey2}\shell\open\command";          ValueType: string; ValueName: "";                 ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes";   ValueType: string; ValueName: "{#MyAppAssocExt2}";             ValueData: ""



[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

