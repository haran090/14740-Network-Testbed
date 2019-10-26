import socket
import numpy as np
import cv2 as cv
import time


addr = ("192.168.2.105", 50000)
buf = 8640
width = 480
height = 270
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk = s.recv(buf)
            print('.')
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)
        try:
        	frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width, 3)
        except Exception as err:
            print(err)
            continue
        cv.imshow('TCP Stream', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()
