__author__ = 'b8horpet'


from NeuralNet.Functions import *


class NeuralObjectInterface:

    Braveness=0.1

    def __init__(self):
        raise PureVirtualCallException()

    def Activate(self):
        raise PureVirtualCallException()

    def Propagate(self):
        raise PureVirtualCallException()
