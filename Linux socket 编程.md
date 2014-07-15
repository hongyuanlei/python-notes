#Linux Socket编程（不限Linux）

我们深谙信息交流的价值，那网络中进程之间如何通信，如我们每天打开浏览器浏览网页时，浏览器的进程怎么与web服务器通信的？当你用QQ聊天时，QQ进程怎么与服务器或你好友所在的QQ进程通信？这些都得靠socket？那什么是socket？socket的类型有哪些？还有socket的基本函数，这些都是本文想介绍的。本文的主要内容如下：

*    网络中进程之间如何通信？
*    socket是什么？
*    socket的基本操作
    *    socket()函数
    *    bind()函数
    *    listen()、connect()函数
    *    accept()函数
    *    read()、write()函数
    *    close()函数
*    socket中TCP的三次握手建立连接详解
*    socket中TCP的四次握手释放连接详解
*    一个例子


