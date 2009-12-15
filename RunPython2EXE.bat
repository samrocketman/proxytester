echo off
title Sam's Autobuilding batch file
cls
REM Compile Executable using a batch file
REM @author: Sam Gleske

REM Here are the things you need to compile this successfully:
REM     Python 2.6 (latest)
REM     py2exe for Python 2.6 (latest)
REM     7-Zip command line utilitiy (make sure 7za.exe is extracted in the same directory as this batch file!)
REM Additional notes:
REM     You will need to add entries to your PATH environment variable (these are examples, not the same on all systems):
REM         C:\python26\ (Python 2.6 directory where python.exe is located)


:: No matter where the batch file is run, run it as if being run from the same dir as RunPython2EXE.bat
%~d0
cd "%~dp0"

:: Version of software: MAJOR.MINOR.PATCHSET
set VERSION=0.5

:: Ask pesky version questions so you don't forget to update them
echo Current MAJOR.MINOR.PATCHSET=%VERSION%
echo Did you update the version number in the following files:
set /p MessageUser="  RunPython2EXE.bat (0.1.PATCHSET) (y/n)?: "
if /I "%MessageUser%" neq "y" Goto End
set MessageUser=""
set /p MessageUser="  Setup.py (0.1.PATCHSET) (y/n)?: "
if /I "%MessageUser%" neq "y" Goto End

:: Clear old binaries and packages
del /s /f /q dist
del /s /f /q packages

:: Compile Windows binary
cd src
python setup.py py2exe
cd ..

:: Put together the distrobution packages
set zip=%~dp07za.exe
mkdir dist
mkdir dist\lists
mkdir packages
copy src\dist\proxytester.exe dist\
copy src\lists\*.* dist\lists\
copy license.txt dist\
copy readme.txt dist\
copy changelog.txt dist\
del /s /f /q "%~dp0src\dist"
del /s /f /q "%~dp0src\build"
cd "%~dp0"
del /s /q *.pyc
cd dist
dir /s /b | "%zip%" a -tzip -xr!*CVS* ..\packages\proxy_tester_win32_v%VERSION%.zip
cd ..
dir /s /b | "%zip%" a -tzip -xr!*CVS* -xr!*dist* -xr!*build* -xr!*packages* -xr!*.exe packages\proxy_tester_v%VERSION%_src.zip

echo Done.
pause
:End