__author__ = 'b8horpet'


from NeuralNet.Common import *


class Neuron(NeuralObjectInterface):
    def __init__(self):
        global ConstantOne
        self.Inputs = []
        self.Output = 0.0
        self.TransferFilter = LinearFilter()
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


class InputNeuron(Neuron):
    def __init__(self):
        self.Output=0.0
        self.Inputs=[0.0]
        self.GetInput=ListValueHolder(self.Inputs)

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
