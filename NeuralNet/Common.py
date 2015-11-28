#author: b8horpet


from NeuralNet.Functions import *


class NeuralObjectInterface:

    Braveness=0.001

    def __init__(self):
        raise NotImplementedError()

    def Activate(self):
        raise NotImplementedError()

    def Propagate(self):
        raise NotImplementedError()
