@ECHO OFF
ECHO Starting Video Stream
START /B python.exe "C:\Users\Public\Documents\Lab2\stream_receive_tcp.py"
START /B python.exe "C:\Users\Public\Documents\Lab2\stream_receive_udp.py"
if errorlevel 1 PAUSE