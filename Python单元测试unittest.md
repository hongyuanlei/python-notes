#单元测试unittest
**1、创建一个简单测试用例**
通过覆盖runTest方法即可得到最简单的测试用例子类以运行一些测试代码：
```Python
 import unittest
 class DefaultWidgetSizeTestCase(unittest.TestCase):
     def runTest(self):
         widget = Widget("The widget")
         assert widget.size() == (50,50), 'incorrect default size'
```
注意：为进行测试，我们只是使用Python内建的`assert`语句。如果在测试用例运行时断言(`assertion`)为假，`AssertionError`异常会被抛出，并且测试框架会认为测试用例失败。其它非`assert`检查所抛出的异常会被测试框架认为是`errors`。
















