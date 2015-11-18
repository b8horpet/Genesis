__author__ = 'b8horpet'


from NeuralNet.Functions import *


class NeuralObjectInterface:
    def __init__(self):
        raise PureVirtualCallException

    def Activate(self):
        raise PureVirtualCallException
