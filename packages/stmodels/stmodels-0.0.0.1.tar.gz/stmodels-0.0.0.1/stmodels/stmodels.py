# For one testing class
class fbnc(object):

    def __init__(self):
        #self._n = n
        pass

    def fib(self,n):
        a, b = 0, 1
        while a < n:
            a, b = b, a + b
        return a


if __name__ == "__main__":
    pass
