# -*- coding:utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import time
import urllib2

urls = [
    'http://www.baidu.com',
    'http://home.baidu.com/',
    'http://tieba.baidu.com/',
    'http://zhidao.baidu.com/',
    'http://music.baidu.com/',
    'http://image.baidu.com/',
    'http://www.qq.com',
    'http://www.youku.com',
    'http://www.tudou.com'
]  

def test1():
    start = time.time()
    results = map(urllib2.urlopen,urls)
    print "Normal:",time.time() - start

def test2():
    start = time.time()
    #开8个worker,没有参数时默认是cpu的核心数
    pool = ThreadPool(processes=8)
    #在线程中执行 urllib2.urlopen(url)并返回执行结果
    results = pool.map(urllib2.urlopen,urls)
    pool.close()
    pool.join()
    print "Thread Pool:",time.time() - start
    
if __name__ == '__main__':
    test1()
    test2()

