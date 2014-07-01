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
这里要注意的一个细节，使用urllib2.install_opener()会设置urllib2的全局opener。这样后面的使用会很方便，但不能做更细粒度的控制，比如想在程序中使用不同的Proxy设置等。比较好的做法是不使用install_opener去更改全局的设置，而只是调用opener的open方法代替全局的urlopen方法。

**2、Timeout设置**

在老版Python中，urllib2的API并没有暴露Timeout的设置，要设置Timeout值，只能更改Socket的全局Timout值。
```Python
import urllib2
import socket

socket.setdefaulttimeout(10) 
urllib2.socket.setdefaulttimeout(10)
```
在Python2.6以后，超时可以通过urllib2.urlopen()的timeout参数直接设置
```Python
import urllib2
response = urllib2.urlopen("http://www.google.com",timeout=10)
```
**3、在HTTP Request中加入特定的Header**

要加入header，需要使用Request对象
```Python
import urllib2
request = urllib2.Request(uri)
request.add_header("User-Agent","fake-client")
response = urllib2.urlopen(request)
```
对有些 header 要特别留意，服务器会针对这些 header 做检查
*    User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
*    Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。常见的取值有：
    *    application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
    *    application/json ： 在 JSON RPC 调用时使用
    *    application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用

在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务

**4、Redirect**

urllib2 默认情况下会针对 HTTP 3XX 返回码自动进行 redirect 动作，无需人工配置。要检测是否发生了 redirect 动作，只要检查一下 Response 的 URL 和 Request 的 URL 是否一致就可以了。
