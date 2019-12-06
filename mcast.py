#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)
# Updated:
#   mcast [-s] multicast_addr path_to_video #sender
#   mcast -r multicast_addr  #receiver

import time
import struct
import socket
import sys

MYPORT = 8123
#MYGROUP_4 = '224.0.3.1' #'127.0.0.1' #
MYGROUP_4=sys.argv[2]
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 1 # Increase to reach other networks
BUFSIZE = 8192*2

#ff='toy.mp4'
try:
    ff=sys.argv[3]
except IndexError:
    rec=1


def main():
    group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4

    if "-s" in sys.argv[1:]:
        sender(group)
    else:
        receiver(group)


def sender(group):
    addrinfo = socket.getaddrinfo(group, None)[0]

    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    #'''
    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    if addrinfo[0] == socket.AF_INET: # IPv4
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
        #s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1000000)

    else:
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
        #s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1000000)

    #'''
    
    with open(ff,'rb') as in_file:        
        while True:
            #data = 'gm' #+ repr(time.time())
            data=in_file.read(BUFSIZE)
            s.sendto(data + '\0', (addrinfo[4][0], MYPORT))
            if data=="":
                break #EOF
            #s.sendto(data)
            time.sleep(0.1) #runs with 0.09 as well


def receiver(group):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 100000000)

    # Bind it to the port
    s.bind(('', MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET: # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        #s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 1000000)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        #s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, 1000000)
        

    fl=open('out.mp4','w')
    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(BUFSIZE)
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        #print (str(sender) + '  ' + repr(data))
        #print (str(repr(data)))
        fl.write(data)
        print data
    fl.close()


if __name__ == '__main__':
    main()
