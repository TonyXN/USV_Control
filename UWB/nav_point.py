#!/usr/bin/env python
# -*- coding: utf-8 -*-


import struct

def toBytes(data):
    splited = str(data).split('#')
    decimal = int(splited[0])+(float(splited[1])/60)+(float(splited[2])/3600)
        
    # print(splited)
    dec = round(decimal, 6)
    # print(decimal)

    ba = bytearray(struct.pack("d",dec))
    data = ''
    for b in ba:
        data += ("\\x%02x" % b)
    return data

def checkSum(data):

    checksum=0
    for i in data.split('\\x')[1:]:

        checksum = int('0x'+i,16)+checksum
    checksum = str("%04x" % checksum)
    return checksum

def returnData(lat_list, lon_list):
    num_point = len(lat_list)
    # print(num_point)
    num_point_bytes = str('\\x%02x' % int(hex(num_point),16))

    header = '\\xff\\x43\\x01\\x7c'
    point_index = '\\x77'
    tail = '\\x0d\\x0a'

    gps_data =''
    for i in range(0, num_point):
        if '#' in lat_list[i]:
            gps_data += point_index+toBytes(lat_list[i])+toBytes(lon_list[i])
        else:
            gps_data += point_index+lat_list[i]+lon_list[i]

    data = header

    data += num_point_bytes + gps_data

    checksum = str(checkSum(data))
    num = '\\x%02x' % int(hex(len(data.split('\\x'))-1),16)
    # print(num)

    data += '\\x'+ checksum[:2]+'\\x'+checksum[2:]+ num + tail
    print(data)
    return data.decode('string_escape')

def main():
    lat_list = ["22#41#13.85"]
    lon_list = ["114#11#33.58"]
    data = returnData(lat_list, lon_list)
    print(data)

if __name__=='__main__':
    main()
