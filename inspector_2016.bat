@echo off
set mayapy="%ProgramFiles%/Autodesk/Maya2016/bin/mayapy.exe"
set mayascript="%~dp0inspector/inspector.py"
set mayafile=%1
%mayapy% %mayascript% %*
pause
