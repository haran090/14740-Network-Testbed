import time
import uuid
import pika

timeout = 10

class Controller(object):

	def on_response(self, ch, method, props, body):
		if self.correlation_id == props.correlation_id:
			self.response = body

	def sendDNSSpoof(self):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='dns_spoof')
		self.channel.basic_publish(exchange='', routing_key='dns_spoof', properties = pika.BasicProperties(), body="start")

	def sendRPCMessage(self, input):
		self.creds = pika.PlainCredentials('admin', 'password')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.creds))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='pipe')
	
		print('Creating callback queue')
		self.response = None
		self.correlation_id = str(uuid.uuid4())
	
		self.result = self.channel.queue_declare('', exclusive=True)
		self.callback_queue = self.result.method.queue
	
		self.channel.basic_consume(queue = self.callback_queue, on_message_callback = self.on_response, auto_ack = True)
		print('Sending Request')
		self.channel.basic_publish(exchange='',
			routing_key='pipe', 
			properties = pika.BasicProperties(reply_to = self.callback_queue, correlation_id = self.correlation_id),
			body=input)

		self.start = time.time()
		while self.response is None:
			time.sleep(1)
			if self.start+timeout < time.time():
				break
			self.connection.process_data_events()
		self.connection.close()
		return self.response