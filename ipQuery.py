#coding:utf-8
import urllib2
import json
import threading

#编码配置,存储ip地址文件的编码
FILE_ENCODING = "gbk"
successList = []
failList = []
successPath = r"success.txt"
failPath = r"failed.txt"
ipPath = "ip.txt"
#一次查询多少个
queryCount = 5
#线程数量配置
threadCount = 5
lock = threading.RLock()
separator = "|"
saveCount = 100
successIndex = 0
failIndex = 0


class IPStruct(object):
    """定义IP的结构内容,包含起始地址,结束地址,地理位置和经纬度"""
    def __init__(self):
        self.startIP = None
        self.endIP = None
        self.address = ""
        self.position = ""
        self.status = ""


class QueryIPLocation(object):
    """传入一个ip对象列表,并将查询到的地理位置和经纬度赋值给相应的ip对象"""
    _retry = 5

    def query(self, objList):
        # 遍历查询
        for obj in objList:
            url = self.get_url(obj).encode('utf-8')
            # 查询数据
            for j in range(0, self._retry + 1):
                result = urllib2.urlopen(url)
                # 查询失败
                if result.getcode() != 200:
                    if j == self._retry:
                        obj.status = "Failed"
                # 查询成功
                else:
                    jsonRet = json.loads(result.read())
                    # 分析数据,这里使用的是百度map-api返回的状态值,具体参考http://developer.baidu.com/map/lbs-appendix.htm#.appendix2
                    if jsonRet['status'] == 0:
                        obj.status = "SUCCESS"
                        self.proc_ok(jsonRet, obj)
                        break
                    elif jsonRet['status'] == 1:
                        obj.status = "SERVER_ERROR"
                        break
                    elif jsonRet['status'] == 2:
                        obj.status = "INVALID_PARAMETER"
                        break
                    elif jsonRet["status"] == 5:
                        obj.status = "INVALID_AK"
                        break
                    elif jsonRet["status"] == 101:
                        obj.status = "DISABLE_SERVICE"
                        break
                    elif jsonRet['status'] == 345:
                        if j == self._retry:
                            obj.status = "MINUTE_QUERY_LIMIT"
                    elif jsonRet["status"] == 355:
                        obj.status = "DAY_QUERY_LIMIT"
                        break

    # 获取地址
    def get_url(self, obj):
        base = "http://api.map.baidu.com/location/ip?ak=7E814968d7b3ee0440678cb17cb4aa29&coor=bd09ll"
        return base + "&ip=" + str(obj.startIP)

    # 获取结果并赋值给obj相应的变量
    def proc_ok(self, result, obj):
        point = result["content"]["point"]
        address = result["content"]["address"]
        obj.address = address
        obj.position = str(point['x']) + "," + str(point['y'])


class MyThread(threading.Thread):
    def __init__(self, queryList):
        threading.Thread.__init__(self)
        self.queryList = queryList

    def run(self):
        global successList
        global failList
        global successIndex
        global failIndex
        app = QueryIPLocation()
        app.query(self.queryList)
        for item in self.queryList:
            if item.status == "SUCCESS":
                lock.acquire()
                successList.append(item)
                successIndex += 1
                lock.release()
                if successIndex == saveCount:
                    lock.acquire()
                    save_result(successPath, failPath, successSequence=successList)
                    successIndex = 0
                    del successList[:]
                    lock.release()
            else:
                lock.acquire()
                failList.append(item)
                failIndex += 1
                lock.release()
                if failIndex >= saveCount:
                    lock.acquire()
                    save_result(successPath, failPath, failSequence=failList)
                    failIndex = 0
                    del failList[:]
                    lock.release()


def read_ip_file(path):
    """读取ip文件并返回ipStruct的列表"""
    ipList = []
    f = open(path)
    if not f:
        print "error open file %s" % path
        return
    for line in f:
        addr = line.split("__")
        count = len(addr)
        #过滤掉特殊行
        if count <= 2 or "." not in addr[0] or "." not in addr[1]:
            continue
        obj = IPStruct()
        obj.startIP = addr[0]
        obj.endIP = addr[1]
        obj.address = addr[2].decode(FILE_ENCODING)
        ipList.append(obj)
    return ipList


def save_result(successPath, failPath, successSequence=[], failSequence=[]):
    """save the success result to successPath, fail result to failPath"""
    global separator
    line = ""
    successFile = open(successPath, "a")
    if not successFile:
        print "error open file %s to write" % successPath
    for item in successSequence:
        line += item.startIP+separator+item.endIP+separator+item.address.encode("utf-8")+separator+item.position+"\n"
    successFile.write(line)
    successFile.close()

    line = ""
    failFile = open(failPath, "a")
    if not failFile:
        print "error open file %s to write" % (failPath)
    for item in failSequence:
        line += item.startIP+separator+item.endIP+separator+item.address.encode("utf-8")+separator+item.status+"\n"
    failFile.write(line)
    failFile.close()


def main():
    global ipPath
    threadList = []
    print "start read file"
    ipList = read_ip_file(ipPath)
    print "end read file"
    count = len(ipList)
    for i in range(0, count, queryCount):
        queryList = ipList[i:i+queryCount]
        t = MyThread(queryList)
        threadList.append(t)
        threadNumber = len(threadList)
        if threadNumber == threadCount:
            for item in threadList:
                item.start()
            for item in threadList:
                item.join()
            del threadList[:]
        print i, "one group thread end"
    #deal withe the left thread list if the thread number is less than global threadCount
    print "remain start"
    for item in threadList:
        item.start()
    for item in threadList:
        item.join()
    print "remain end"
    save_result(successPath, failPath, successSequence=successList, failSequence=failList)
    print "all done"

if __name__ == "__main__":
    main()



