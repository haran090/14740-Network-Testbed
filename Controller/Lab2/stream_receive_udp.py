import socket
import numpy as np
import cv2 as cv


addr = ("192.168.0.10", 60000)
buf = 8644
width = 480
height = 270
code = b'start'
num_of_chunks = (int)(width * height * 3 / (buf-4))

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    error = False
    start = False
    while True:
        chunks = []
        if not error:
            start = False
        else:
            error = False

        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if not chunk.startswith(code):
                if start:
                	chunks.insert(int(chunk[:4]), chunk[4:])
            elif not start:
                start = True

        byte_frame = b''.join(chunks)
        #print(len(byte_frame))
        try:
            frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width, 3)
            cv.imshow('UDP Stream', frame)
        except:
            print("Error")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()
