@echo off
set mayapy="%ProgramFiles%/Autodesk/Maya2014/bin/mayapy.exe"
set mayascript="%~dp0inspector/inspector.py"
set mayafile=%1
%mayapy% %mayascript% --solve %*
pause
