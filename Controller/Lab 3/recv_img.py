import socket
import numpy as np
import cv2 as cv
import time
import sys
from PyQt5.QtWidgets import *


addr = ("128.237.136.94", 5555)

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(addr)
	sock.listen(1)
	chunks = []
	print("Listening")
	con,client = sock.accept()
	
	while len(chunks) < 54211:
		chunk = con.recv(1460)
		chunks.append(chunk)

	try:
		byte_frame = b''.join(chunks)
		byte_arr = np.frombuffer(byte_frame, np.uint8)
		image = cv.imdecode(byte_arr, cv.IMREAD_COLOR)
		image = cv.resize(image, (500, 500))
		cv.imshow('New message', image)

		sock.close()
	except Exception as err:
		print("TCP ERROR -- ")
		print(err)

	while True:
		if cv.waitKey(1) & 0xFF == ord('q'):
			break
