import socket
import numpy as np
import cv2 as cv
import time

addr_tcp = ("192.168.2.105", 55000)
addr_udp = ("192.168.0.10", 65000)
buf = 4096
image = cv.imread('/home/pi/image.jpg',-1)
data = cv.imencode('.jpg', image)[1].tostring()
    
if __name__ == '__main__':
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_tcp.bind(addr_tcp)
    s_tcp.listen(1)    
    while True:
            try:			
                print("Listening...")
                con,client = s_tcp.accept()
                print("Conntected")
                for i in range(0, len(data), buf):
                    con.send(data[i:i+buf])
                    s_udp.sendto(str((int)(i/buf)).zfill(4).encode()+data[i:i+buf], addr_udp) 
                con.close()
                print("Terminated")
            except Exception as err:
                print("Fatal Error")
                print(err)
                time.sleep(1)
        
