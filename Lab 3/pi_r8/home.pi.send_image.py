import socket
import numpy as np
import cv2 as cv
import time

addr = ("3.0.0.1", 5555)
buf = 4096
image = cv.imread('/home/pi/image.jpg',-1)
data = cv.imencode('.jpg', image)[1].tostring()
    
if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(addr)
            print("Conntected")
            for i in range(0, len(data), buf):
                con.send(data[i:i+buf])
            con.close()
            print("Terminated")
        except Exception as err:
            print("Could not connect. Trying again in 5 seconds")
            print(err)
            time.sleep(5)
        
