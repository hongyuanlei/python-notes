#使用multiprocessing.dummy执行多线程任务

`multiprocessing.dummy`模块与`multiprocessing`模块的区别：`dummy`模块是多线程，而`multiprocessing`是多进程,api都是通用的。所以可以很方便将代码在多线程和多进程之间切换。

Python实现并行化--日常多线程操作的新思路

Python 在程序并行化方面多少有些声名狼藉。撇开技术上的问题，例如线程的实现和 GIL，我觉得错误的教学指导才是主要问题。常见的经典 Python 多线程、多进程教程多显得偏“重”。而且往往隔靴搔痒，没有深入探讨日常工作中最有用的内容。

**1、传统的例子**
```Python
import time 
import threading 
import Queue 
class Consumer(threading.Thread): 
    def __init__(self, queue): 
        threading.Thread.__init__(self)
        self._queue = queue 

    def run(self):
        while True: 
            # queue.get() blocks the current thread until 
            # an item is retrieved. 
            msg = self._queue.get() 
            # Checks if the current message is 
            # the "Poison Pill"
            if isinstance(msg, str) and msg == 'quit':
                # if so, exists the loop
                break
            # "Processes" (or in our case, prints) the queue item   
            print "I'm a thread, and I received %s!!" % msg
        # Always be friendly! 
        print 'Bye byes!'


def Producer():
    # Queue is used to share items between
    # the threads.
    queue = Queue.Queue()

    # Create an instance of the worker
    worker = Consumer(queue)
    # start calls the internal run() method to 
    # kick off the thread
    worker.start() 

    # variable to keep track of when we started
    start_time = time.time() 
    # While under 5 seconds.. 
    while time.time() - start_time < 5: 
        # "Produce" a piece of work and stick it in 
        # the queue for the Consumer to process
        queue.put('something at %s' % time.time())
        # Sleep a bit just to avoid an absurd number of messages
        time.sleep(1)

    # This the "poison pill" method of killing a thread. 
    queue.put('quit')
    # wait for the thread to close down
    worker.join()


if __name__ == '__main__':
    Producer()
```
哈，看起来有些像 Java 不是吗？

我并不是说使用生产者/消费者模型处理多线程/多进程任务是错误的（事实上，这一模型自有其用武之地）。只是，处理日常脚本任务时我们可以使用更有效率的模型。

**问题在于...**

   首先，你需要一个样板类;
   其次，你需要一个队列来传递对像;
   而且，你还需要在通道两端都构建相应的方法来协助其工作（如果需想要进行双向通信或是保存结果还需要再引入一个队列）。

**worker 越多，问题越多**

按照这一思路，你现在需要一个worker线程池。下面是一篇IBM经典教程中的例子--在进行网页检索时通过多线程进行加速。

```Python
#Example2.py
'''
A more realistic thread pool example 
'''

import time 
import threading 
import Queue 
import urllib2 

class Consumer(threading.Thread): 
    def __init__(self, queue): 
        threading.Thread.__init__(self)
        self._queue = queue 

    def run(self):
        while True: 
            content = self._queue.get() 
            if isinstance(content, str) and content == 'quit':
                break
            response = urllib2.urlopen(content)
        print 'Bye byes!'


def Producer():
    urls = [
        'http://www.python.org', 'http://www.yahoo.com'
        'http://www.scala.org', 'http://www.google.com'
        # etc.. 
    ]
    queue = Queue.Queue()
    worker_threads = build_worker_pool(queue, 4)
    start_time = time.time()

    # Add the urls to process
    for url in urls: 
        queue.put(url)  
    # Add the poison pillv
    for worker in worker_threads:
        queue.put('quit')
    for worker in worker_threads:
        worker.join()

    print 'Done! Time taken: {}'.format(time.time() - start_time)

def build_worker_pool(queue, size):
    workers = []
    for _ in range(size):
        worker = Consumer(queue)
        worker.start() 
        workers.append(worker)
    return workers

if __name__ == '__main__':
    Producer()

```

