#!/usr/bin/env python
'''receiver ROS Node'''
import rospy
from nlink.msg import node_frame2
import nav_point
import socket
import time

global flag 
flag = False
def callback(data):
    global flag
    '''receiver Callback Function'''
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.distances)
    rospy.loginfo("\nPosition:\n%s \nAngle:\n%s \n", data.position, data.angle)
    
    # pos = data.position.x
    # print(type(pos))

    dis = ((data.position.x)**2 + (data.position.y)**2 + (data.position.z)**2)**0.5

    print 'Dis:',dis
    # flag = False    #False for manual control
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)
    udp_socket.bind(("",9876))
    recv_ip = "10.23.123.209"
    recv_port = 9876

    if flag == False and dis >= 5:  #离开停泊区域
        flag = True
        # lat_list = ["22#41#13.85"]
        # lon_list = ["114#11#33.58"]
        # data = nav_point.returnData(lat_list, lon_list)
        data = '\xff\x43\x00\x7c\x00\x98\x01\xa0\x01\x39\x0d\x0a'   #极小速度前进
        auto_data = '\xff\x43\x03\x7c\xc2\x0d\x0a'
        udp_socket.sendto(auto_data,("10.23.123.209",9876))
        # time.sleep(0.5)
        udp_socket.sendto(data,("10.23.123.209",9876))

        udp_socket.close()
        print "AUTO MODE\nsocket closed ......"

    elif flag == True and dis <= 5: #进入停泊区域
        flag = False
        data = '\xff\x43\x00\x7c\x00\x98\x01\x98\x01\x31\x0d\x0a'   #原地待命
        udp_socket.sendto(data,("10.23.123.209",9876))

        udp_socket.close()
        print "MANUAL MODE\Nsocket closed ......"
    print flag

        
def main():

    rospy.init_node('receiver', anonymous=True)
    rospy.Subscriber("nlink_linktrack_nodeframe2", node_frame2, callback)
    time.sleep(0.5)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

   


if __name__=='__main__':
    main()

