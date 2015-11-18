__author__ = 'b8horpet'


import math


Derivatives = {}


class PureVirtualCallException(Exception):
    pass


class FunctionObjectInterface:
    def __init__(self):
        raise PureVirtualCallException

    def __call__(self, *args, **kwargs):
        raise PureVirtualCallException


class LinearFilter:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return args[0]


class SlabFilter:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        if args[0] > 0.0:
            return 1.0
        else:
            return -1.0


class LinearSlabFilter:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        x=args[0]
        if x > 1.0:
            return 1.0
        elif x < -1.0:
            return -1.0
        else:
            return x


#sigmoids -- easy to differentiate
class TangentHyperbolic:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return math.tanh(args[0])


class ConstZero:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return 0.0


class ConstOne:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return 1.0


class ConstValueHolder:
    def __init__(self, v):
        self.value = v

    def __call__(self, *args, **kwargs):
        return self.value


class ListValueHolder:
    def __init__(self, l):
        self.value = l

    def __call__(self, *args, **kwargs):
        return self.value[0]


class Polinomial:
    def __init__(self,n: int, a: float = 1.0):
        self.n = n
        self.a = a

    def __call__(self, x: float, *args, **kwargs):
        return self.a * ( x**self.n )

    def __str__(self):
        return "f(x)="+str(self.a)+"*x^"+str(self.n)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return (self.n,self.a) == (other.n,other.a)

for i in range(1,3):
    Derivatives[Polinomial(i)]=Polinomial(i-1,i)
