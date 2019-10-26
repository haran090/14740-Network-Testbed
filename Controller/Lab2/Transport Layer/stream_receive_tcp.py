import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65534)
buf = 15360
width = 1920
height = 1080
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
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)
        try:
        	frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width, 3)
        except:
        	# print("Error")
        	continue
        cv.imshow('TCP Stream', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()
