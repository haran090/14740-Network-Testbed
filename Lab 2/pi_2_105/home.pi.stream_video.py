import socket
import numpy as np
import cv2 as cv
import time

addr_tcp = ("192.168.2.105", 50000)
addr_udp = ("192.168.0.10", 60000)
buf = 8640
width = 480
height = 270
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')
time.sleep(1)

if __name__ == '__main__':
	s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s_udp.setsockopt(socket.IPPROTO_IP, 10, 2)

	s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s_tcp.bind(addr_tcp)
	s_tcp.listen(1)
	while True:
		try:			
			print("Listening...")
			#count = 0
			con,client = s_tcp.accept()
			print("Conntected")
			cap = cv.VideoCapture(0)
			cap.set(3, 1920)
			cap.set(4, 1080)
			while(cap.isOpened()):
				ret, frame = cap.read()
				#==================Control frame rate by skipping frame. 0 skip = 30fps				
				#count += 1
				#if count%3 == 0:
				#	continue
				frame = cv.resize(frame, (width, height))
				if ret:
					s_udp.sendto(code, addr_udp)
					con.send(code)
					data = frame.tostring()
					#print(len(data))
					for i in range(0, len(data), buf):
						s_udp.sendto(str((int)(i/buf)).zfill(4).encode()+data[i:i+buf], addr_udp)
						con.send(data[i:i+buf])
				else:
					break
			con.close()
			print("Terminated")
		except:
			print("Fatal Error")
			time.sleep(1)
		finally:
			if cap:
				cap.release()
