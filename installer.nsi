OutFile "nsis_test.exe"

Var SourceFiles
Var InstallToPath


Section  
    StrCpy $SourceFiles "$EXEDIR\build"
    StrCpy $InstallToPath "$EXEDIR\installer-dump"

    

    CreateDirectory "$InstallToPath"
    MessageBox MB_YESNO "Install on $InstallToPath ?" IDYES lYes IDNO lNo

    lYes:
        CopyFiles "$SourceFiles\*" "$InstallToPath" 1000
        Goto jump
    lNo:
        MessageBox MB_OK "Goodbye!"
        Goto jump

    jump:


SectionEnd
