import socket
import numpy as np
import cv2 as cv

addr = ("127.0.0.1", 65535)
buf = 4096
start = 'start'
start = ('start' + (buf - len(start) + 4) * 'a').encode('utf-8')

if __name__ == '__main__':
    image = cv.imread('image.jpg',-1)
    # image = cv.resize(image, (960, 540))
    # cv.imshow('Image over UDP', image)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = cv.imencode('.jpg', image)[1].tostring()
    while True:
        s.sendto(start, addr)
        for i in range(0, len(data), buf):
            s.sendto(str((int)(i/buf)).zfill(4).encode()+data[i:i+buf], addr)