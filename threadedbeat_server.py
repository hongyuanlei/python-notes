# -*- coding:utf-8 -*-

"""多线程 heartbeat 服务器"""

import socket,threading,time
PORT = 43278
HOST = ""
CHECK_PERIOD = 20
CHECK_TIMEOUT = 15

class Heartbeats(dict):
    """用线程锁管理共享的heartbeats字典"""
    def __init__(self):
        super(Heartbeats,self).__init__()
        self._lock = threading.Lock()
    def __setitem__(self,key,value):
        """为客户端创建或更新字典中的条目"""
        self._lock.acquire()
        try:
            super(Heartbeats,self).__setitem__(key,value)
        finally:
            self._lock.release()
    def get_silent(self):
        """返回沉默期长于CHECK_TIMEOUT的客户端列表"""
        limit = time.time() - CHECK_TIMEOUT
        self._lock.acquire()
        try:
            silent = [ip for (ip,ipTime) in self.items() if ipTime < limit]
        finally:
            self._lock.release()
        return silent

class Receiver(threading.Thread):
    """接收UDP包并将其记录在heartbeats字典中"""
    def __init__(self,goOnEvent,heartbeats):
        super(Receiver,self).__init__()
        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats
        self.rec_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#        self.rec_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.rec_socket.settimeout(CHECK_TIMEOUT)
        self.rec_socket.bind((HOST,PORT))
    def run(self):
        while self.goOnEvent.isSet():
            try:
                data,addr = self.rec_socket.recvfrom(5)
                if data == 'PyHB':
                    self.heartbeats[addr[0]] = time.time()
            except socket.timeout as e:
                print e

def main(num_receivers=1):
    receiver_event = threading.Event()
    receiver_event.set()
    heartbeats = Heartbeats()
    receivers = []
    for i in range(num_receivers):
        receiver = Receiver(goOnEvent=receiver_event,
                            heartbeats=heartbeats)
        receiver.start()
        receivers.append(receiver)
    print("Threaded heartbeat server listening on PORT %d" % PORT)
    print("press Ctrl-C to stop")
    try:
        while True:
            silent = heartbeats.get_silent()
            print("Silent clients:%s" % silent)
            time.sleep(CHECK_PERIOD)
    except KeyboardInterrupt:
        print('Exiting,please wait ...')
        receiver_event.clear()
        for receiver in receivers:
            receiver.join()
        print("Finished")

if __name__ == '__main__':
    main()
        
            
