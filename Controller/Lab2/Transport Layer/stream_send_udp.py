import socket
import numpy as np
import cv2 as cv

addr = ("192.168.0.200", 65535)
buf = 10800
width = 240
height = 135
cap = cv.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
code = 'start'
code = ('start' + (buf - len(code) + 4) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = cv.resize(frame, (width, height))
        if ret:
            s.sendto(code, addr)
            # print('Start')
            data = frame.tostring()
            # print(len(data))
            for i in range(0, len(data), buf):
                s.sendto(str((int)(i/buf)).zfill(4).encode()+data[i:i+buf], addr)
            # cv.imshow('send', frame)
            # if cv.waitKey(1) & 0xFF == ord('q'):
            #     break
        else:
            break
    # s.close()
    # cap.release()
    # cv.destroyAllWindows()
