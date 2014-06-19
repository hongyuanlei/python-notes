# -*- coding:utf-8 -*-

"""heartbeat客户端"""

import socket,time
SERVER_IP = "127.0.0.1"
SERVER_PORT = 43278
BEAT_PERIOD = 5
print("Sending heartbeat to IP %s,PORT %d" % (SERVER_IP,SERVER_PORT))
print("press Ctrl-C to stop")

while True:
    heartbeat_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    heartbeat_socket.sendto('PyHB',(SERVER_IP,SERVER_PORT))
    if __debug__:
        print('Time:%s' % time.ctime())
    time.sleep(BEAT_PERIOD)
