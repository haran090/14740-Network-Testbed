import socket
import numpy as np
import cv2 as cv
import time
import sys
from PyQt5.QtWidgets import *


addr = ("192.168.2.105", 55000)
buf = 4096
code = b'start'

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    chunks = []
    while True:
        chunk = s.recv(buf)
        chunks.append(chunk)
        if len(chunks) >= 989051:
            break

    byte_frame = b''.join(chunks)
    try:
        byte_arr = np.frombuffer(byte_frame, np.uint8)
        image = cv.imdecode(byte_arr, cv.IMREAD_COLOR)
        image = cv.resize(image, (960, 540))
        cv.imshow('Image over TCP', image)
    except Exception as err:
        print("TCP ERROR -- ")
        print(err)
       
    s.close()
    
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cv.destroyAllWindows()
