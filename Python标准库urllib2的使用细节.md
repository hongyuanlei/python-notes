#Python标准库urllib2的使用细节

python标准库中有很实用的工具类，但是在具休使用时，标准库文档上对使用细节描述的并不清楚，比如urllib2这个Http客户端库。这里总结了一些urllib2的使用细节。
*    Proxy的设置
*    Timeout设置
*    在Http Request中加入特定的Header
*    Redirect
*    Cookie
*    使用HTTP的PUT和DELETE方法
*    得到HTTP的返回码
*    Debug Log

**1、Proxy的设置**
urllib2默认会使用环境变量http_proxy来设置HTTP Proxy。如果想在程序中明确控制Proxy而不受环境变量的影响，可以使用下面的方式
```Python
import urllib2
enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http":"http://some-proxy.com:8080"})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)
```
