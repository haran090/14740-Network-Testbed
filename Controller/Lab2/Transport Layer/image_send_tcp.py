import socket
import numpy as np
import cv2 as cv

addr = ("127.0.0.1", 65532)
buf = 4096

if __name__ == '__main__':
    image = cv.imread('image.jpg',-1)
    data = cv.imencode('.jpg', image)[1].tostring()
    while True:
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind(addr)
	    s.listen(1)
	    con,client = s.accept()
	    for i in range(0, len(data), buf):
	        con.send(data[i:i+buf])
	    con.close()
	    if cv.waitKey(1) & 0xFF == ord('q'):
	    	break
        