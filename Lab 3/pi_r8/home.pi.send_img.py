import socket
import numpy as np
import cv2 as cv
import time

addr = ("128.237.136.94", 5555)
image = cv.imread('img.jpg',-1)
data = cv.imencode('.jpg', image)[1].tostring()
print(str(len(data)) + " bytes")
if __name__ == '__main__':
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(addr)
            print("Connected.")
            s.sendall(data)
            print("Terminated")
        except Exception as err:
            print("Could not connect. Trying again in 5 seconds")
            print(err)
            time.sleep(5)
