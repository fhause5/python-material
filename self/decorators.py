from datetime import datetime

def timeit(arg):
    print(arg)
    def returnDecorator(func):
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            print(datetime.now() - start)
            return result
        return wrapper
    return returnDecorator

@timeit('Starting')
def one(n):
    l = []
    for i in range(n):
        if i % 2 == 0:
            l.append(i)
    return l


l1 = timeit('Starting')(one)(10)
