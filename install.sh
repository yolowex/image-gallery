here=`pwd`
echo $here
# done: fix the file associations not getting added
# done: fix the program not appearing in the search menu

buildPath="$here/build"
assetsPath="$here/test_assets"
pythonEntryPath="$here/main.py"
installerPath="$here/installer"
installerOutPath="$installerPath/inno.iss"
shouldBuildExe=0
shouldBuildInstaller=0
extentions=("jpg" "myp2" "mid5")

appName="Foto Folio"
appVersion="1.0"
appPublisher="Great Sunshine Company"
appUrl="https://github.com/Arthur378"
appExeName="Foto Folio.exe"
appAssocName="$appName File"
# this should probably be more dynamic
exeSource="../build/Foto Folio.exe"

write_assoc_def() {
    number=$1
    extention=$2
    outputfile=$3
    echo "writing definition section for" $extention

    
assoc_def=$(cat <<EOF
;
#define MyAppAssocExt$number "$extention"
#define MyAppAssocKey$number StringChange(MyAppAssocName, " ", "") + MyAppAssocExt$number
EOF
    )

    echo "$assoc_def" >> $outputfile
}

write_assoc_reg() {
    number=$1
    extention=$2
    outputfile=$3
    echo "writing registry section for" $extention
    
    assoc_reg=$(cat <<EOF
;
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt$number}\OpenWithProgids";             ValueType: string; ValueName: "{#MyAppAssocKey$number}"; ValueData: "";                     Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey$number}";                             ValueType: string; ValueName: "";                 ValueData: "{#MyAppAssocName}";    Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey$number}\DefaultIcon";                 ValueType: string; ValueName: "";                 ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey$number}\shell\open\command";          ValueType: string; ValueName: "";                 ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes";  ValueType: string; ValueName: "{#MyAppAssocExt$number}";             ValueData: ""

EOF
    )

    echo "$assoc_reg" >> $outputfile
}

write_installer_script()
{

    echo Starting to write the inno setup script
    echo writing the definition section for inno setup

    def_section_text=$(cat <<EOF
#define MyAppName "$appName"
#define MyAppVersion "$appVersion"
#define MyAppPublisher "$appPublisher"
#define MyAppURL "$appUrl"
#define MyAppExeName "$appExeName"
#define MyAppAssocName "$appAssocName"
#define ExeSource "$exeSource"
EOF
    )


    if [ -e $installerOutPath ]; then
        rm $installerOutPath
    else
        echo 
    fi


    echo "$def_section_text" >> $installerOutPath

    echo writing the definition section for program\'s associated extentions

    i=0
    for item in "${extentions[@]}"; do
        write_assoc_def $i ".$item" $installerOutPath
        ((i++))
    done

body_section_text=$(cat <<EOF
; 
[Setup]
AppId={{931B78F1-4C54-4E34-883F-1470C64243CB}}
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
; 
EOF
    )


    echo "$body_section_text" >> $installerOutPath
    
    echo "[Registry]" >> $installerOutPath
    
    echo writing the registeration section for program\'s associated extentions 

    i=0
    for item in "${extentions[@]}"; do
        write_assoc_reg $i ".$item" $installerOutPath
        ((i++))
    done



final_section_text=$(cat <<EOF
[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

EOF
    )

    echo writing the final section of the inno setup script!
    echo "$final_section_text" >> $installerOutPath
}

if [ -e $buildPath ]; then
    echo The build folder already exists, re-build the executables?? y/n:  
    read input

    if [ "$input" == "y" ]; then
        shouldBuildExe=1
    elif [ "$input" == "n" ]; then
        echo Ok
    else
        echo Bad output! 1>&2
        exit 1
    fi

else
    echo The build folder does not exist.
    shouldBuildExe=1
fi


if [ -e $installerPath ]; then
    echo The installer folder already exists, re-build the Windows Installer?? y/n:  
    read input

    if [ "$input" == "y" ]; then
        shouldBuildInstaller=1
    elif [ "$input" == "n" ]; then
        echo Ok
    else
        echo Bad output! 1>&2
        exit 1
    fi
else
    echo The installer folder does not exist.
    shouldBuildInstaller=1
fi


if [ $shouldBuildExe -eq 1 ]; then
    echo "Building the executables ..."
    rm -rf $buildPath
    mkdir $buildPath
    cd $buildPath
    echo "I'm in $(pwd)"
    pyinstaller $pythonEntryPath --onefile

    rm -rf "$buildPath\build"
    rm "$buildPath\main.spec"
    # todo: automatically sync the executable name with the script name ( or sth like that )
    mv "$buildPath\dist\main.exe" "$buildPath\\$appExeName"
    rm -r "$buildPath\dist"
    cp -r $assetsPath $buildPath

else
    echo "The executables are already built."
fi

if [ $shouldBuildInstaller -eq 1 ]; then
    echo "Building the Windows Installer ..."
    rm -rf $installerPath
    mkdir $installerPath
    write_installer_script
else
    echo "The Windows Installer is already built."
fi


echo -e "\nGoodbye!"
