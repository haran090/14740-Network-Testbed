import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65532)
buf = 4096
code = b'start'

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    chunks = []
    while True:
        chunk = s.recv(buf)
        chunks.append(chunk)
        if len(chunk) < buf:
            break

    byte_frame = b''.join(chunks)
    try:
        byte_arr = np.frombuffer(byte_frame, np.uint8)
        image = cv.imdecode(byte_arr, cv.IMREAD_COLOR)
        image = cv.resize(image, (960, 540))
        cv.imshow('Image over UDP', image)
    except Exception as err:
        print(err)

    s.close()
    
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cv.destroyAllWindows()
