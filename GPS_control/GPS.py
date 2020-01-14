from __future__ import division
import struct

def gps2dec(degree,minute,second):
    minute/=60
    second/=3600
    value = round(minute+degree+second,6)
    return value

def dec2hex(value):     #convert float to 8 bytes hex number
    a_list = []
    b_list = []
    ba = bytearray(struct.pack("d",value))
    print struct.unpack('d',ba)[0]
    hexData = ["0x%02x" % b for b in ba]
    return hexData

def countChecksum(cmd): #use the previous oct numbers as inputs to calculate checkSum
    checksum = 0
    for i in cmd:
        checksum += int(i,16)
    #print hex(checksum)
    return hex(checksum)

def inputHandle():
    desList = []
    index = ['0x77']
    targetP = int(input("Enter the number of destinations:"))
    count = 1
    while count <= targetP:
        if count % 10 == 1:
            countToken = str(count) + 'st'
        elif count % 10 == 2:
            countToken = str(count) + 'nd'
        elif count % 10 == 3:
            countToken = str(count) + 'rd'
        else:
            countToken = str(count) + 'th'
        print "Enter the {order} group of latitude info".format(order=countToken)
        degree = input("du:")
        degree = int(degree)
        minute = int(input("fen:"))
        second = float(input("miao:"))
        latitude = gps2dec(degree, minute, second)
        hexLa = dec2hex(latitude)
        desList = desList + index + hexLa
        print "Enter the {order} group of longitude info".format(order=countToken)
        degree = int(input("du:"))
        minute = int(input("fen:"))
        second = float(input("miao:"))
        longitude = gps2dec(degree, minute, second)
        hexLo = dec2hex(longitude)
        desList = desList + hexLo
        count += 1
    return desList, targetP

def main():
    received_pos = []
    infoTuple = inputHandle()
    header = ['0xff', '0x43', '0x01', '0x7c']
    ender = ['0x0D', '0x0A']
    points = infoTuple[1]
    #points = 2
    ######two locs on the lake for test
    #['0x77','0x62', '0x6f', '0x4f', '0x7d', '0xd', '0xb0', '0x36', '0x40', '0xb8', '0x94', '0xf3', '0xc5', '0x5e', '0x8c', '0x5c', '0x40','0x77', '0x47', '0x9', '0xe7', '0x40', '0xfc', '0xaf', '0x36', '0x40','0xa7', '0x3b', '0x4f', '0x3c', '0x67', '0x8c', '0x5c', '0x40']
    frame = [hex(4+1+17*(points))]
    firstHalfCmd = header + [hex(points)] +infoTuple[0]
    #print firstHalfCmd
    checkSum = countChecksum(firstHalfCmd)
    #print checkSum
    if len(checkSum) == 6:
        firstCheckSum = '0x' + checkSum[2:4]
        secondCheckSUm = '0x' + checkSum[4:6]
    elif len(checkSum) == 5:
        firstCheckSum = '0x0' + checkSum[2]
        secondCheckSUm = '0x' + checkSum[3:5]
    secondHalfCmd = [firstCheckSum,secondCheckSUm] + frame + ender
    #print secondHalfCmd
    cmd = firstHalfCmd + secondHalfCmd
    #print cmd
    cmd = [struct.pack('B',int(i,16)) for i in cmd]
    cmd = "".join(cmd)
    #print cmd
    for i in cmd:
	received_pos.append(struct.unpack('B',i)[0])
    received_pos = [hex(i) for i in received_pos]
    print(received_pos)
    return cmd



if __name__ == '__main__':
    main()
