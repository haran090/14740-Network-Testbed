import time
import uuid
import pika

timeout = 10

class Controller(object):

	def on_response(self, ch, method, props, body):
		print('Response received')
		if self.correlation_id == props.correlation_id:
			self.response = body

	def censor(self):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='censor')
		self.channel.basic_publish(exchange='', routing_key='censor', properties = pika.BasicProperties(), body="start")
		print('Censor trigger sent')

	def runIperfTest(self):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='iperf')
		self.channel.basic_publish(exchange='', routing_key='iperf', properties = pika.BasicProperties(), body="start")
		print('IPERF trigger sent')

	def changeLoss_IPERF(self, loss):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='iperf')
		self.channel.basic_publish(exchange='', routing_key='iperf', properties = pika.BasicProperties(), body=str(loss))
		print('Loss change trigger sent to Iperf server - '+str(loss))

	def changeLoss_VID(self, loss):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='vid_server')
		self.channel.basic_publish(exchange='', routing_key='vid_server', properties = pika.BasicProperties(), body=str(loss))
		print('Loss change trigger sent to video server - '+str(loss))

	def doRPC(self):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='iperf')
	
		print('Starting Remote Procedure Call')
		self.response = None
		self.correlation_id = str(uuid.uuid4())
	
		self.result = self.channel.queue_declare('iperf_resp', exclusive=True)
		self.callback_queue = self.result.method.queue
	
		self.channel.basic_consume(queue = self.callback_queue, on_message_callback = self.on_response, auto_ack = True)
		print('Sending Request')
		self.channel.basic_publish(exchange='',
			routing_key='iperf', 
			properties = pika.BasicProperties(reply_to = self.callback_queue, correlation_id = self.correlation_id),
			body="iperf")

		self.start = time.time()
		while self.response is None:
			time.sleep(1)
			if self.start+timeout < time.time():
				break
			self.connection.process_data_events()
		self.connection.close()
		return self.response