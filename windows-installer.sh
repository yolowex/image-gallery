here=`pwd`
echo $here
# done: fix the file associations not getting added
# done: fix the program not appearing in the search menu
# todo: fix the program's icon not being shown in the search menu

command="iscc"
iscc_exists=0
if where "$command" > /dev/null 2>&1; then
    iscc_exists=1
else
    echo "Warning: Could not find iscc, please install Inno Setup Compiler"
    echo " or if you have it installed already, add it to PATH"
fi


buildPath="$here/build"
iconPath="$here/assets/icon.png"
pythonEntryPath="$here/main.py"
installerPath="$here/installer"
installerOutPath="$installerPath/inno.iss"
shouldBuildExe=0
shouldBuildInstaller=0
extensions=("jpg" "gif" "webp" "png" "mp4" "mkv" "avi" )
source_dirs=("assets" "ffmpeg")
appName="Lotus"
appVersion="1.0"
appPublisher="Arthur378"
appUrl="https://github.com/Arthur378"
appExeName="Lotus.exe"
appAssocName="$appName File"
# this should probably be more dynamic
exeSource="../build/Lotus.exe"



add_source_dir() {
    number=$1
    dir_name=$2
    outputfile=$3
    echo "adding" $dir_name "source directory in app's installation folder"

mkdir_section=$(cat <<EOF
Name: "{app}\\$dir_name"
EOF
    )

    echo "$mkdir_section" >> $outputfile
    
}

add_source_def() {
    number=$1
    dir_name=$2
    outputfile=$3
    echo "adding source definition for" $dir_name

dirdef_section=$(cat <<EOF
Source: "../$dir_name/*"; DestDir: "{app}\\$dir_name"; Flags: ignoreversion recursesubdirs createallsubdirs
EOF
    )

    echo "$dirdef_section" >> $outputfile
}

write_assoc_def() {
    number=$1
    extension=$2
    outputfile=$3
    echo "writing definition section for" $extension
    
assoc_def=$(cat <<EOF
;
#define MyAppAssocExt$number "$extension"
#define MyAppAssocKey$number StringChange(MyAppAssocName, " ", "") + MyAppAssocExt$number
EOF
    )

    echo "$assoc_def" >> $outputfile
}

write_assoc_reg() {
    number=$1
    extension=$2
    outputfile=$3
    echo "writing registry section for" $extension
    
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

    echo writing the definition section for program\'s associated extensions

    i=0
    for item in "${extensions[@]}"; do
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
OutputBaseFilename=Lotus Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
EOF
    )

    echo "$body_section_text" >> $installerOutPath

    i=0
    for item in "${source_dirs[@]}"; do
        add_source_dir $i $item $installerOutPath
        ((i++))
    done
    
file_section_text=$(cat <<EOF
;
[Files]
Source: "{#ExeSource}" ; DestDir: "{app}"; Flags: ignoreversion
EOF
)

    echo "$file_section_text" >> $installerOutPath

    i=0
    for item in "${source_dirs[@]}"; do
        add_source_def $i $item $installerOutPath
        ((i++))
    done

    echo "[Registry]" >> $installerOutPath
    
    echo writing the registeration section for program\'s associated extensions

    i=0
    for item in "${extensions[@]}"; do
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
    if [ -e $buildPath ]; then
        rm -rf $buildPath
        echo Deleting $buildPath
    else
        echo $buildPath does not exist.
    fi

    mkdir $buildPath
    cd $buildPath
    echo "I'm in $(pwd)"
    pyinstaller $pythonEntryPath --onefile --icon=$iconPath 

    rm -rf "$buildPath\build"
    rm "$buildPath\main.spec"
    # todo: automatically sync the executable name with the script name ( or sth like that )
    mv "$buildPath\dist\main.exe" "$buildPath\\$appExeName"
    rm -r "$buildPath\dist"

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


if [ $iscc_exists -eq 0 ]; then
    echo Could not find iscc \(Inno Setup Compiler\), I can\'t compile the installer
else 
    echo Compile the Inno Setup Script file?? y/n:  
    read input

    if [ "$input" == "y" ]; then
        iscc $installerOutPath 
    elif [ "$input" == "n" ]; then
        echo Ok
    else
        echo Bad output! 1>&2
        exit 1
    fi
fi

echo -e "\nGoodbye!"
