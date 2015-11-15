__author__ = 'b8horpet'


from NeuralNet.Common import *
import math


def LinearFilter(x: float) -> float:
    return x


def SlabFilter(x: float) -> float:
    if x > 0.0:
        return 1.0
    else:
        return -1.0


def LinearSlabFilter(x: float) -> float:
    if x > 1.0:
        return 1.0
    elif x < -1.0:
        return -1.0
    else:
        return x

#sigmoids -- easy to differentiate
def TangentHyperbolic(x: float) -> float :
    return math.tanh(x)


class Neuron(NeuralObjectInterface):
    def __init__(self):
        global ConstantOne
        self.Inputs = []
        self.Output = 0.0
        self.TransferFilter = LinearFilter
#        self.TransferFilter = LinearSlabFilter
        Synapsis(ConstantOne, self, 0.0)

    def __del__(self):
        pass

    def Activate(self):
        _sum = 0.0
        for i in self.Inputs:
            i.Activate()
            _sum += i.Weight*i.Current
        self.Output=self.TransferFilter(_sum)


def ConstZero() -> None:
    return 0


def ConstValueHolder(x):
    def HolderFunction():
        return x
    return HolderFunction


def ValueHolder(x):
    def HolderFunction():
        return x[0]
    return HolderFunction


class InputNeuron(Neuron):
    def __init__(self):
        self.Output=0.0
        self.Inputs=[0.0]
        self.GetInput=ValueHolder(self.Inputs)

    def Activate(self):
        self.Inputs[0]=self.GetInput()
        self.Output=self.Inputs[0]


class HiddenNeuron(Neuron):
    pass


class OutputNeuron(Neuron):
    pass


class ConstantNeuron(NeuralObjectInterface):
    def __init__(self):
        self.Output=1.0

    def __del__(self):
        pass

    def Activate(self):
        pass


class Synapsis:
    def __init__(self, begin: Neuron = None, end: Neuron = None, weight: float = 1.0):
        self.From = begin
        self.To = end
        self.Weight = weight
        self.Current = self.From.Output
        self.To.Inputs.append(self)

    def __del__(self):
        pass

    def Activate(self):
        self.Current = self.From.Output

ConstantOne = ConstantNeuron()

print("Neuron class imported")
