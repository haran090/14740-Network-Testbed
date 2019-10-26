import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65535)
buf = 15364
width = 1920
height = 1080
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
            else:
                error = True
                break
        if error:
            print("Error 1")
            continue

        byte_frame = b''.join(chunks)
        print(len(byte_frame))
        try:
            frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(height, width, 3)
            frame = cv.resize(frame, (960, 540))
            cv.imshow('UDP Stream', frame)
        except:
            print("Error 2")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()
