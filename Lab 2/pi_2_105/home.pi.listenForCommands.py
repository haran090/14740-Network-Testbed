import pika
import time
import os

min_loss = '0.0000000232'

def rpc_callback(ch, method, properties, body):
	print('RPC recvd')
	response = "Success" 
	prop = pika.BasicProperties(correlation_id=properties.correlation_id)
	ch.basic_publish(exchange = '', routing_key = properties.reply_to, properties=prop,body=response)


def callback(ch, method, properties, body):
	print('Command recvd')
	try:
		float(body)   
		if body == '0.0':
			body = min_loss        
		print('Changing packet loss to ' + body + '%')
		os.system("sudo tc qdisc change dev eno1 root netem loss "+body+"%")
	except:
		print('Invalid parameter')

os.system("sudo tc qdisc add dev eno1 root netem loss "+min_loss+"%")
creds = pika.PlainCredentials('admin', 'password')
while(True):
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.10', 5672, '/', creds))
		break
	except:
		print('Could not connect to MQTT server. Retrying in 2 seconds.')
		time.sleep(2)
channel = connection.channel()
channel.queue_declare(queue='vid_server')

channel.basic_consume(queue='vid_server', on_message_callback=callback, auto_ack=True)
print('Waiting......')
channel.start_consuming()
