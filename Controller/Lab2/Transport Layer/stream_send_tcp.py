import socket
import numpy as np
import cv2 as cv

addr = ("127.0.0.1", 65534)
buf = 12288
width = 1280
height = 720
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    while True:
        con,client = s.accept()
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                con.send(code)
                data = frame.tostring()
                print(len(data))
                for i in range(0, len(data), buf):
                    con.send(data[i:i+buf])
                # cv.imshow('send', frame)
                # if cv.waitKey(1) & 0xFF == ord('q'):
                #     break
            else:
                break
        con.close()
    # s.close()
    # cap.release()
    # cv.destroyAllWindows()
