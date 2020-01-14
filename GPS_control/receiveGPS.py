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

def shou(udp_socket):
    # usv_data = create_string_buffer(56)
    while not rospy.is_shutdown():
        received_pos = []
        print "starting receiving data ..."
        (usv_data, addr)= udp_socket.recvfrom(1024)
        print len(usv_data)
        for i in usv_data:
            received_pos.append(struct.unpack('B', i)[0])
        received_pos = [hex(i) for i in received_pos]
        print received_pos
        hexLatitude = usv_data[5:13]
        latitude = struct.unpack('d', hexLatitude)
        hexLongitude = usv_data[14:22]
        longitude = struct.unpack('d', hexLongitude)
        print 'weidu:', latitude[0]
        print 'jingdu:', longitude[0]
        if len(received_pos) == 43: #data returned from manual mode
            pass ###reserved for info decryption
        elif len(received_pos) == 72: #data returned from auto mode
            pass
        print "shoushoushou"
        time.sleep(0.1)

def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)
    udp_socket.bind(("",9876))
    recv_ip = "10.23.123.209"
    recv_port = 9876
    state = "ok"
    rospy.init_node('receiveGPS', anonymous = True)
    #autoMode(udp_socket)
    #t2 = threading.Thread(target=shou, args=(udp_socket,))
    #t1 = threading.Thread(target=fa, args=(udp_socket,))
    #t1.setDaemon(True)
    #t2.setDaemon(True)
    #t1.start()
    #t2.start()
    while not rospy.is_shutdown():
        #cancelNav(udp_socket)
        shou(udp_socket)
        print "1111"
        time.sleep(1)
        #pub.publish(gps(state, x, y))
    udp_socket.close()
    print "socket closed ......"

if __name__=='__main__':
    main()
