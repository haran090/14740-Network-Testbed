from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
import random
import string

def randomString():
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for i in range(16))

random_cookie = ''

class Server(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.send_header('Hint','Try sending a POST')
		self.end_headers()
		self.wfile.write(b'<html><head><link rel="icon" href="data:,"></head><h1>Welcome!</h1><body>There is a flag somewhere in this page.\n\nCan you find it?</body></html>')

	
	def do_POST(self):
		len = int(self.headers['Content-Length'])
		params = self.rfile.read(len).decode('utf-8')
		body = {}
		try:
			body = {params.split('=')[0].strip().upper():params.split('=')[1].strip()}
			print(body)
		except Exception as err:
			print(err)

		if params and 'COOKIE' in body and body['COOKIE'] == random_cookie:
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.end_headers()
			response = BytesIO()
			value =  b'<html><head><link rel="icon" href="data:,"></head><h1>Success!</h1><body>Here\'s your flag, "14740rocks{_POST_IS_EASY_}"</body></html>'
			response.write(value)
			self.wfile.write(response.getvalue())
		else:
			self.send_response(403)
			self.send_header('Content-Type', 'text/html')
			self.end_headers()
			response = BytesIO()
			value =  b'<html><meta name="cookie" content="'
			value = b"".join([value, random_cookie.encode()])
			value2 = b'"><head><link rel="icon" href="data:,"></head><h1>No secret? No flag!</h1><body>You clearly don\'t know the secret. Maybe wireshark will help?</body></html>'
			value = b''.join([value, value2])
			response.write(value)
			self.wfile.write(response.getvalue())

random_cookie = randomString()
httpd = HTTPServer(('10.0.0.84', 80), Server)
httpd.serve_forever()
