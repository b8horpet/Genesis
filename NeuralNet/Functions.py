#author: b8horpet


import math


class FunctionObjectInterface:
    def __init__(self):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    def __eq__(self, other):
        return isinstance(other,type(self))

    def Differentiate(self):
        return None


class LinearFilter(FunctionObjectInterface):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return args[0]

    def Differentiate(self):
        return ConstOne()


class SlabFilter(FunctionObjectInterface):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        if args[0] > 0.0:
            return 1.0
        else:
            return -1.0


class LinearSlabFilter(FunctionObjectInterface):
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
class TangentHyperbolic(FunctionObjectInterface):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return math.tanh(args[0])

    def Differentiate(self):
        class OneminusTanhSquared(FunctionObjectInterface):
            def __init__(self):
                pass

            def __call__(self, *args, **kwargs):
                return 1.0-(math.tanh(args[0])**2)
        return OneminusTanhSquared()


class ConstZero(FunctionObjectInterface):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return 0.0

    def Differentiate(self):
        return ConstZero()


class ConstOne(FunctionObjectInterface):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return 1.0

    def Differentiate(self):
        return ConstZero()


class ConstValueHolder(FunctionObjectInterface):
    def __init__(self, v):
        self.value = v

    def __call__(self, *args, **kwargs):
        return self.value

    def Differentiate(self):
        return ConstZero()


class ListValueHolder(FunctionObjectInterface):
    def __init__(self, l):
        self.value = l

    def __call__(self, *args, **kwargs):
        return self.value[0]

    def Differentiate(self):
        return ConstZero()


class Polinomial(FunctionObjectInterface):
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
        #for now
        return isinstance(other,type(self)) and (self.n,self.a) == (other.n,other.a)

    def Differentiate(self):
        return Polinomial(self.n-1,self.a*self.n)
