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

**4、将测试用例聚合成测试套件**

测试用例实例可以根据它们所测试的特性组合到一起。PyUnit为此提供了一个机制叫做“测试套件”(test suite)。它由unittest模块中的TestSuite类表示：
```
widgetTestSuite = unittest.TestSuite()
widgetTestSuite.addTest(WidgetTestCase("testDefaultSize"))
widgetTestSuite.addTest(WidgetTestCase("testResize"))
```
我们稍后会看到，在每一个测试模块中提供一个返回已经创建测试套件的可调用对象，会是一个使测试更加便捷的好方法：
```Python
def suite():
       suite = unittest.TestSuite()
       suite.addTest(WidgetTestCase("testDefaultSize"))
       suite.addTest(WidgetTestCase("testResize"))
       return suite
```

甚至可写成：
```Python
class WidgetTestSuite(unittest.TestSuite):
    def  __init__(self):
        unittest.TestSuite.__init__(self,map(WidgetTestCase,
                                                               ("testDefaultSize","testResize")))
```
(诚然，第二种方法不是为胆小者准备的)因为创建一个包含很多相似名称的测试方法的TestCase子类是一种很常见的模式，所以unittest模块提供一个便捷方法，`makeSuite`来创建一个由测试用例类内所有测试用例组成的测试套件：
```
suite = unittest.makeSuite(WidgetTestCase,'test')
```
需要注意的是，当使用makeSuite方法时，测试套件运行每个测试用例的顺序是由测试方法名根据Python内建函数`cmp`所排序的顺序而决定的。

**5、嵌套测试套件**

我们经常希望将一些测试套件组合在一起来一次性的测试整个系统。这很简单，因为多个TestSuite可以被加入进一个TestSuite，就如同多个TestCase被加进一个TestSuite中一样：
```Python
suite1 = module1.TheTestSuite()
suite2 = module2.TheTestSuite()
alltest = unittest.TestSuite((suite1,suite2))
```
在发布的软件包中的“examples”目录中，"alltests.py”提供了使用嵌套测试套件的例子。

**6、测试代码放置的位置**

你可以将测试用例定义与被测试代码置于同一个模块中（例如“widget.py”），但是将测试代码放置在单独的模块中（如：“widgettests.py”）会有一些优势：
*    测试模块可以从命令行单独执行
*    测试代码可以方便地从发布代码中分离
*    少了在缺乏充足理由的情况下为适应被测试代码而更改测试代码的诱惑
*    被测试代码可以更方便的进行重构
*    如果测试策略改变，也无需修改被测试源代码

**7、交互式运行测试**
我们编写测试的主要目的是运行它们并检查我们的软件是否工作正常。测试框架使用“TestRunner”类来为运行测试提供环境。最常用的TestRunner是TextTestRunner，它可以以文字方式运行测试并报告结果：
```
runner = unittest.TextTestRunner(0
runner.run(widgetTestSuite)
```
TextTestRunner默认将输出发送到sys.stderr，但是你可以通过向它的构造传递一个不同的类似文件(file-object)对象来改变默认方式。如需要在Python解释器会话中运行测试，这样使用TextTestRunner是一个理想的方法。

**8、命令行运行测试**

unittest模块包含一个main方法，可以方便地将测试模块转变为可以运行测试的脚本。main 使用unittest.TestLoader类来自动查找和加载模块内测试用例。

因此，如果你之前已经使用test*惯例对测试方法进行命名，那么你就可以将以下代码插入测试模块的结尾：
```
if __name__ == '__main__':
    unittest.main()
```
这样，当你从命令行执行你的测试模块时，其所包含的所有测试都将被运行。使用“-h”选项运行模块可以查看所有可用的选项。

如需从命令行运行任意测试，你可以将unittest模块作为脚本运行，并将所需执行的测试套件中的测试用例名称作为参数传递给此脚本：
```Shell
% python unittest.py widgettests.WidgetTestSuite
 % python unittest.py widgettests.makeWidgetTestSuite
```
你还可以在命令行指明特定的测试（方法）来执行。如要运行“listtests”模块中的TestCase类的子类 'ListTestCase'（参见发布软件包中的“examples”子目录）， 你可以执行以下命令：
```Shell
 % python unittest.py listtests.ListTestCase.testAppend
```
“testAppend”是测试用例实例将要执行的测试方法的名称。你可以执行以下代码来创建ListTestCase类实例并执行其所包含的所有“test*”测试方法：
```Shell
 % python unittest.py listtests.ListTestCase
```










