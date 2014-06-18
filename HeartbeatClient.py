"""Heartbeat客户端，周期性发送UDP包"""

import socket,time

SERVER_IP = "10.10.190.58"
SERVER_PORT = 50007
BEAT_PERIOD = 5

print("Sending heartbeat to IP:{0},PORT:{1}".format(SERVER_IP,SERVER_PORT))
print("Press Ctrl-C to stop")

while True:
    hbSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    hbSocket.sendto(b"PyHB",(SERVER_IP,SERVER_PORT))
    if __debug__:
        print("Time:%s" % time.ctime())
    time.sleep(BEAT_PERIOD)


