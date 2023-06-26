OutFile "nsis_test.exe"
Var InstPath 

Section  
    StrCpy $InstPath "$DESKTOP\image-gallery\installer-dump"

    MessageBox MB_YESNO "messagebox_text $EXEDIR"

    MessageBox MB_OK "Let's make a file in $InstPath"

    FileOpen $0 "$InstPath\test_file.txt" "w"
    FileWrite $0 "sometext$\r$\n on multiple lines"
    FileClose $0

    Exec "mkdir $InstPath\test_shell"
    Exec "ping google.com"
    MessageBox MB_OK "Installation succsessfull!"

SectionEnd


Section

    MessageBox MB_YESNO "Do you want to proceed with the installation? $EXEDIR" IDYES Label_Yes IDNO Label_No

Label_Yes:
    ; User clicked "Yes"
    MessageBox MB_OK "User clicked Yes."
    Goto Label_End

Label_No:
    ; User clicked "No"
    MessageBox MB_OK "User clicked No."
    Goto Label_End

Label_End:
    ; Perform other operations or continue with the installation
SectionEnd

; Section

;   ; Read Python installation path from registry
;   ReadRegStr $0 HKLM "SOFTWARE\Python\PythonCore\{desired_version}\InstallPath" "InstallPath"

;   ; Check if Python installation path exists
;   StrCmp $0 "" NotInstalled FoundInstalled

;   NotInstalled:
;     MessageBox MB_OK "Python is not installed."
    

;   FoundInstalled:
;     MessageBox MB_OK "Python is installed at: $0"
;     ; Continue with the installation process or perform desired actions

; SectionEnd