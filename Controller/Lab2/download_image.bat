@ECHO OFF
ECHO Starting Image Download
START /B python.exe "C:\Users\Public\Documents\Lab2\image_receive_udp.py"
START /B python.exe "C:\Users\Public\Documents\Lab2\image_receive_tcp.py"
if errorlevel 1 PAUSE