# Python 对 JSON的相关操作

**1、对简单数据类型的encoding和decoding:**

使用简单的json.dumps方法对简单数据类型进行编码，例如：

```Python
import json
obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
encodedjson = json.dumps(obj)
print repr(obj)
print encodedjson
```
输出：
```Shell
[[1, 2, 3], 123, 123.123, 'abc', {'key2': (4, 5, 6), 'key1': (1, 2, 3)}] 
[[1, 2, 3], 123, 123.123, "abc", {"key2": [4, 5, 6], "key1": [1, 2, 3]}]
```
通过输出的结果可以看出，简单类型通过encode之后跟其原始的repr()输出结果非常相似，但是有些数据类型进行了改变，例如上例中的元组则转换为了列表。在json的编码过程中，会存在从python原始类型向json类型的转化过程，具体的转化对照如下：

Python         JSON
*    dict ------> object
*    list,tuple ------> array
*    str,unicode ------> string
*    int,long,float ------> number
*    True ------> true
*    False ------> false
*    None ------> null   

json.dumps()方法返回了一个str对象encodedjson,我们接下来对encodedjson进行decode，得到原始数据，需要使用json.loads()函数：

```Python
decodejson = json.loads(encodedjson)
print type(decodejson)
print decodejson[4]['key1']
print decodejson
```
输出：
```Shell
<type 'list'> 
[1, 2, 3]
[[1, 2, 3], 123, 123.123, u'abc', {u'key2': [4, 5, 6], u'key1': [1, 2, 3]}]
```









