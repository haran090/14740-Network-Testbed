$ORIGIN com.
@	1	IN	SOA	ns.tld.com.	haran.sivaram.	4 1 10 1 1
	IN	NS	ns.tld.com.
ns.tld.com.	IN	A	192.168.1.106

cool.com.	IN	NS	ns.cool.com.
ns.cool.com.	IN	A	192.168.1.108

ctf.game.com.	IN	NS	ns.game.com.
game.com.	IN	NS	ns.game.com.	
ns.game.com.	IN	A	192.168.1.103

bill.com.	A	192.168.1.102
google.com.	A	192.168.1.102
amazon.com.	A	192.168.1.102

