#author: b8horpet


from NeuralNet.Functions import *


class NeuralObjectInterface:

    Braveness=0.001

    def __init__(self):
        raise PureVirtualCallException()

    def Activate(self):
        raise PureVirtualCallException()

    def Propagate(self):
        raise PureVirtualCallException()
