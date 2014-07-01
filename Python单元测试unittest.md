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

运行测试用例的方法会在后介绍。现在我们只是通过调用无参数的构造器来创建一个测试用例的实例：
```
testCase = DefaultWidgetSizeTestCase()
```
**2、复用设置代码：创建固件**

现在，这样的测试用例数量巨大且它们的设置需要很重复性工作。在上面的测试用例中，如若100个Widget测试用例的每一个子类中都创建一个“Widget”，那会导致难看的重复。幸运的是，我们可以将这些设置代码提取出来放置在一个叫做`setUp`的钩子方法(hook method)中。测试框架会在运行测试时自动调用此方法：
```Python
import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget("The widget")

class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
    def runTest(self):
        assert self.widget.size() == (50,50), 'incorrect default size'

class WidgetResizeTestCase(SimpleWidgetTestCase):
	def runTest(self):
		self.widget.resize(100,150)
		assert self.widget.size() == (100,150),\
			   'wrong size after resize'
```
如果`setUp`方法在测试运行时抛出异常，框架会认为测试遇到了错误并且runTest不会被执行。类似的，我们也可以提供一个`tearDown`方法来完成在runTest运行之后的清理工作：
```Python
import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget("The widget")
    def tearDown(self):
    	self.widget.dsipose()
    	self.widget = None
```
如果`setUp`执行成功能，那么无论runTest是否成功，tearDown方法都将被执行。

**3、包含多个测试方法的测试用例类**

很多小型测试用例经常会使用相同的固件。在这个用例中，我们最终从SimpleWidgetTestCase继承产生很多仅包含一个方法的类，如DefaultWidgetSizeTestCase。这是很耗时且不被鼓励的，因此，沿用JUnit的风格，PyUnit提供了一个更简便的方法：
```Python
import unittest
class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget("The widget")
    def tearDown(self):
        self.widget.dispose()
        self.widget = None
    def testDefaultSize(self):
        assert self.widget.size() == (50,50), 'incorrect default size'
    def testResize(self):
        self.widget.resize(100,150)
        assert self.widget.size() == (100,150), \
               'wrong size after resize'0),\
	   'wrong size after resize'     
```
在这个用例中，我们没有提供runTest方法，而是两个不同的测试方法。类实例将创建和销毁各自的self.widget并运行某一个test方法。当创建类实例时，我们必须通过向构造器传递方法的名称来指明哪个测试方法将被运行：
```
defaultSizeTestCase = WidgetTestCase("testDefaultSize")
resizeTestCase = WidgetTestCase("testResize")
```














