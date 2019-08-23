import pika
import time
import os

min_loss = '0.0000000232'

def rpc_callback(ch, method, properties, body):
	print('RPC recvd')
	response = "Success" 
	prop = pika.BasicProperties(correlation_id=properties.correlation_id)
	ch.basic_publish(exchange = '', routing_key = properties.reply_to, properties=prop,body=response)


def iperf_callback(ch, method, properties, body):
    print('Command recvd')    
    if 'start' in body:    
        print('Starting IPERF test')
        os.system("/home/pi/iperf_test")
    else:
        if body == '0.0':
            body = min_loss        
        print('Changing packet loss to ' + body + '%')
        os.system("sudo tc qdisc change dev eth0 root netem loss "+body+"%")

creds = pika.PlainCredentials('admin', 'password')
while(True):
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.10', 5672, '/', creds))
		break
	except:
		print('Could not connect to MQTT server. Retrying in 2 seconds.')
		time.sleep(2)
channel = connection.channel()
channel.queue_declare(queue='iperf')

channel.basic_consume(queue='iperf', on_message_callback=iperf_callback, auto_ack=True)
print('Waiting......')
channel.start_consuming()
