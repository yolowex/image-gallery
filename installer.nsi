!include nsDialogs.nsh

OutFile "nsis_test.exe"

Var SourceFiles
Var InstallToPath
Var APP_NAME 
Var APP_VERSION
Var APP_PUBLISHER

Section  
    StrCpy $SourceFiles "$EXEDIR\build"
    StrCpy $InstallToPath "$EXEDIR\installer-dump"

    StrCpy $APP_NAME "Foto Folio"
    StrCpy $APP_VERSION "1.0.0"
    StrCpy $APP_PUBLISHER "Great Northern Software Co"

    ; nsDialogs::SelectFolderDialog "Select path" "C:\"

    CreateDirectory "$InstallToPath"
    MessageBox MB_YESNO "Install on $InstallToPath ?" IDYES lYes IDNO lNo
    WriteRegStr HKCU "Software\Microsoft\Windows\$APP_PUBLISHER\$APP_NAME" "" "$InstallToPath"

    lYes:
        CopyFiles "$SourceFiles\*" "$InstallToPath" 1000
        Goto jump
    lNo:
        MessageBox MB_OK "Goodbye!"
        Goto jump

    jump:


SectionEnd
