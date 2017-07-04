Python内置了一些非常有趣但非常有用的函数，充分体现了Python的语言魅力！
filter(function, sequence)：对sequence中的item依次执行function(item)，\
function的返回值只能是True或Fals，将执行结果为True的item组成一个List/String/Tuple（取决于sequence的类型）返回：
>>> def f(x): return x % 2 != 0 and x % 3 != 0
>>> filter(f, range(2, 25))
[5, 7, 11, 13, 17, 19, 23]
map(function, sequence) ：对sequence中的item依次执行function(item)，\
见执行结果组成一个List返回：
>>>def doub(x): return x + x
>>>map(doub , "abcde")
['aa', 'bb', 'cc', 'dd', 'ee']
reduce(function, sequence, starting_value)：对sequence中的item顺序迭代调用function，\
如果有starting_value，还可以作为初始值调用，function接收的参数个数只能为2，例如可以用来对List求和：
>>> def add(x,y): return x + y
>>> reduce(add, range(1, 5))
10 （注：(((1+2)+3)+4）)
>>> reduce(add, range(1, 5), 20)
75 （注：(((1+2)+3)+4)+20）
lambda：这是Python支持一种有趣的语法，它允许你快速定义单行的最小函数，\
类似与C语言中的宏，这些叫做lambda的函数，是从LISP借用来的，可以用在任何需要函数的地方：
>>> g = lambda x: x * 2
>>> g(3)
6
>>> (lambda x: x * 2)(3)
6
>>> g = lambda x, y : x + y
>>> reduce(g,range(10))
45 （注：0+1+2+3+4+5+6+7+8+9）

