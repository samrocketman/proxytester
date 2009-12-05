REM Compile Executable using a batch file
REM @author: Sam Gleske
REM @created: November 30th, 2009

REM Here are the things you need to run this successfully:
REM 	Python 2.6 (latest)
REM Additional notes:
REM 	You will need to add entries to your PATH environment variable (these are examples, not the same on all systems):
REM 		C:\python26\ (Python 2.6 directory where python.exe is located)


echo off
title Generating wpad.dat and refined proxylist.txt

:: No matter where the batch file is run, run it as if being run from the same dir as RunPython2EXE.bat
%~d0
cd %~dp0
cls

python check-status-proxy-address.py
del /q /s *.pyc
echo Updating the refined list
del proxylist.txt
copy new_list.txt proxylist.txt
del new_list.txt

echo Updating uploadable wpad.dat
del "D:\My Websites\current\wpad.dat"
copy wpad.dat "D:\My Websites\current\wpad.dat"
echo Done.
pause