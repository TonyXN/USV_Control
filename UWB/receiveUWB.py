#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''receiver ROS Node'''
import rospy
from nlink.msg import node_frame1
import nav_point
import socket
import time
import re

global flag, time
flag = 0
time = 0

def callback(data):
    global flag, time
    '''receiver Callback Function'''
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.distances)
    # rospy.loginfo("\nPosition:\n%s \n", data.nodes)
    if data.nodes == []:
        # print 'WTFFFFFFFFFFFFFFFFFFFFFFFFF'
        pass
    else:
        pos = re.split('\n|:|]', str(data.nodes))[6:12]
        # print pos

        # x = float(pos[1])
        # y = float(pos[3])
        # z = float(pos[5])
        # print x, y, z

        dis = ((float(pos[1]))**2 + (float(pos[3]))**2)**0.5
        # print 'Dis:', dis
        if time == 0:
            flag = -1 if dis <= 1 else 1 if dis >= 5 else 0
            time = 1
        elif time <= 10:
            time += 1
        else:
            time = 1
            sendtoBoat(dis)


def sendtoBoat(dis):
    global flag

    print '-'*15
    print 'Dis:',dis
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)
    udp_socket.bind(("",9876))
    recv_ip = "10.23.123.209"
    recv_port = 9876

    if flag == 0 and dis >= 5:  #离开停泊区域
        flag = 1
        # lat_list = ["22#41#13.85"]
        # lon_list = ["114#11#33.58"]
        # data = nav_point.returnData(lat_list, lon_list)
        # data = '\xff\x43\x00\x7c\x00\x98\x01\x9b\x01\x34\x0d\x0a'   #极小速度前进
        auto_data = '\xff\x43\x03\x7c\xc2\x0d\x0a'  #切换自动
        udp_socket.sendto(auto_data,("10.23.123.209",9876))
        # time.sleep(0.5)
        # udp_socket.sendto(data,("10.23.123.209",9876))

        # udp_socket.close()
        print "....AUTO MODE....\n"

    elif flag == 1 and dis <= 5: #进入停泊区域
        flag = 0
        # data = '\xff\x43\x00\x7c\x00\x98\x01\x98\x01\x31\x0d\x0a'   #原地待命
        data = '\xff\x43\x00\x7c\x00\x98\x01\xa0\x01\x39\x0d\x0a'   #极小速度前进
        # data = '\xff\x43\x00\x7c\x00\x98\x01\x8c\x01\x25\x0d\x0a'   #极小速度后退
        stop_data = '\xff\x43\x07\x7c\xc6\x0d\x0a'  #取消导航
        udp_socket.sendto(stop_data,("10.23.123.209",9876))
        udp_socket.sendto(data,("10.23.123.209",9876))
        # udp_socket.close()
        print "....MANUAL MODE....\n"

    elif flag == 0 and dis <= 1:  
        flag = -1
        data = '\xff\x43\x00\x7c\x00\x98\x01\x98\x01\x31\x0d\x0a'   #原地待命
        udp_socket.sendto(data,("10.23.123.209",9876))

        print "....INTO THE HARBOR..."
    
    elif flag == -1 and dis >= 1:
        flag = 0
        data = '\xff\x43\x00\x7c\x00\x98\x01\x8c\x01\x25\x0d\x0a'   #极小速度后

        auto_data = '\xff\x43\x03\x7c\xc2\x0d\x0a'  #切换自动
        # udp_socket.sendto(auto_data,("10.23.123.209",9876))
        # time.sleep(0.5)
        udp_socket.sendto(data,("10.23.123.209",9876))

        # udp_socket.close()
        print "....LEAVING THE HARBOR..."

    print 'Flag:', flag

    print '='*15


def main():

    rospy.init_node('receiver', anonymous=True)
    rospy.Subscriber("nlink_linktrack_nodeframe1", node_frame1, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__=='__main__':
    main()

