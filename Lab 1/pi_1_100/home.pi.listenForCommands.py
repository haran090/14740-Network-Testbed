import pika
import requests
import time
import json
import os

def callback(ch, method, properties, body):
	os.system("sudo python dns_spoof.py")

creds = pika.PlainCredentials('admin', 'password')
while(True):
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.10', 5672, '/', creds))
		break
	except:
		print('Could not connect to MQTT server. Retrying in 2 seconds.')
		time.sleep(2)
channel = connection.channel()
channel.queue_declare(queue='dns_spoof')

channel.basic_consume(queue='dns_spoof', on_message_callback=callback, auto_ack=True)
print('Waiting......')
channel.start_consuming()
