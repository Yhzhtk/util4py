# coding=utf-8

# Python 装饰器实现DRY(不重复代码)原则

def increment(f):
    def wrapped_f(args,a2):
        c = f(args,a2)
        c = int(c)
        c += 3
        print c
        return c
    return wrapped_f

def increment1(f):
    def wrapped_f(args,a2):
        c = f(args,a2)
        c = int(c)
        c += 1
        print c
        return c
    return wrapped_f

def increment2(f):
    def w(a1,a2):
        print f(1,3)
        return f(a1,a2) + 1
    return w


@increment1
@increment
@increment2
def plus(a, b):
    c = a + b
    return c

result = plus(4, 6)
print result
