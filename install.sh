here=`pwd`
echo $here

buildPath="$here/build"
assetsPath="$here/test_assets"
pythonEntryPath="$here/main.py"
installerPath="$here/installer"
shouldBuildExe=0
shouldBuildInstaller=0


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
    mv "$buildPath\dist\main.exe" "$buildPath\main.exe"
    rm -r "$buildPath\dist"
    cp -r $assetsPath $buildPath

else
    echo "The executables are already built."
fi

if [ $shouldBuildInstaller -eq 1 ]; then
    echo "Building the Windows Installer ..."
    rm -rf $installerPath
    mkdir $installerPath
else
    echo "The Windows Installer is already built."
fi


