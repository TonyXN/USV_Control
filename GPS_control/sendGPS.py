#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import socket
import rospy
from usv_communication.msg import gps
import threading
import time
import struct
from ctypes import create_string_buffer
import GPS

#global x
#global y
received_pos = []
#info = GPS.main()
#for i in info:
    #received_pos.append(struct.unpack('B',i)[0])
#received_pos = [hex(i) for i in received_pos]
#for i in range(len(received_pos)):
    #if len(received_pos[i]) == 3:
        #received_pos[i] = received_pos[i][0:2] + '0' + received_pos[i][-1]
#print received_pos

def fa(udp_socket):
    data = GPS.main()
    #data = '\xff\x42\x00\x7c\x00\x90\x01\x93\x01\x24\x0d\x0a'
    print "fafafafafa"
    udp_socket.sendto(data,("10.23.123.209",9876))
    time.sleep(0.5)

# def shou(udp_socket):
#     print "ssss"
#     global x
#     x = 1
#     # usv_data = create_string_buffer(56)
#     while not rospy.is_shutdown():
#         received_pos = []
#         print "starting receiving data ..."
#         (usv_data, addr)= udp_socket.recvfrom(1024)
#         print len(usv_data)
#         for i in usv_data:
#             received_pos.append(struct.unpack('B', i)[0])
#         received_pos = [hex(i) for i in received_pos]
#         print received_pos
#         x = x+1
#         print "shoushoushou"
#         time.sleep(0.1)

def autoMode(udp_socket):
    chmodCMD = '\xff\x43\x03\x7c\xc2\x0d\x0a'
    udp_socket.sendto(chmodCMD, ("10.23.123.209", 9876))
def cancelNav(udp_socket):
    cmd = '\xff\x43\x07\x7c\xc6\x0d\x0a'
    udp_socket.sendto(cmd, ("10.23.123.209", 9876))
def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)
    udp_socket.bind(("",9876))
    recv_ip = "10.23.123.209"
    recv_port = 9876
    state = "ok"
    rospy.init_node('sendGPS', anonymous = True)

    autoMode(udp_socket)
    #t2 = threading.Thread(target=shou, args=(udp_socket,))
    #t1 = threading.Thread(target=fa, args=(udp_socket,))
    #t1.setDaemon(True)
    #t2.setDaemon(True)
    #t1.start()
    #t2.start()
    while not rospy.is_shutdown():
        #cancelNav(udp_socket)
        autoMode(udp_socket)
        fa(udp_socket)
        print "1111"
        time.sleep(1)
        #pub.publish(gps(state, x, y))
    udp_socket.close()
    print "socket closed ......"

if __name__=='__main__':
    main()
