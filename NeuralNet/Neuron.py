#author: b8horpet


from NeuralNet.Common import *


class Neuron(NeuralObjectInterface):
    def __init__(self):
        global ConstantOne
        self.Inputs = []
        self.Output = 0.0
        self.Sum = 0.0
        self.eps=0.0
        self.TransferFilter = TangentHyperbolic()
#        self.TransferFilter = LinearFilter()
#        self.TransferFilter = LinearSlabFilter
        Synapsis(ConstantOne, self, 0.0)

    def Activate(self):
        _sum = 0.0
        for i in self.Inputs:
            i.Activate()
            _sum += i.Weight*i.Current
        self.Sum=_sum
        self.Output=self.TransferFilter(self.Sum)

    def Propagate(self):
        dtf=self.TransferFilter.Differentiate()
        for i in self.Inputs:
            i.eps=self.eps*dtf(self.Sum)
            i.Propagate()
        self.eps=0.0


class InputNeuron(Neuron):
    def __init__(self):
        self.Output=0.0
        self.Inputs=[0.0]
        self.eps=0.0
        self.GetInput=ListValueHolder(self.Inputs)

    def Activate(self):
        self.Inputs[0]=self.GetInput()
        self.Output=self.Inputs[0]

    def Propagate(self):
        self.eps=0.0


class HiddenNeuron(Neuron):
    pass


class OutputNeuron(Neuron):
    pass


class ConstantNeuron(NeuralObjectInterface):
    def __init__(self):
        self.Output=1.0
        self.eps=0.0

    def Activate(self):
        pass

    def Propagate(self):
        self.eps=0.0


class Synapsis(NeuralObjectInterface):
    def __init__(self, begin: Neuron = None, end: Neuron = None, weight: float = 1.0):
        self.From = begin
        self.To = end
        self.Weight = weight
        self.eps=0.0
        self.Current = self.From.Output
        self.To.Inputs.append(self)

    def Activate(self):
        self.Current = self.From.Output

    def Propagate(self):
        self.From.eps+=self.eps*self.Weight
        self.Weight+=self.Braveness*self.eps*self.Current
        self.eps=0.0


class FixedSynapsis(Synapsis):
    def Propagate(self):
        # don't have to know, what propagate function exactly does
        W=self.Weight
        Synapsis.Propagate(self)
        self.Weight=W


ConstantOne = ConstantNeuron()

print("    Neuron class imported")
