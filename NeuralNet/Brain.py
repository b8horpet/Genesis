__author__ = 'b8horpet'


from NeuralNet.Common import *


class NeuronLayer(NeuralObjectInterface):
    def __init__(self):
        self.Neurons=[]

    def __del__(self):
        pass

    def Activate(self):
        for i in self.Neurons:
            i.Activate()

    def Propagate(self):
        for i in self.Neurons:
            i.Propagate()


class Brain(NeuralObjectInterface):
    def __init__(self):
        self.InputLayer=NeuronLayer()
        self.OutputLayer=NeuronLayer()
        self.HiddenLayers=[]

    def __del__(self):
        pass

    def Activate(self):
        self.InputLayer.Activate()
        for i in self.HiddenLayers:
            i.Activate()
        self.OutputLayer.Activate()

    def Propagate(self, Expected):
        if len(Expected) != len(self.OutputLayer.Neurons):
            raise Exception()
        for i in range(0,len(Expected)):
            currN=self.OutputLayer.Neurons[i]
            #error=0.5*(Expected[i]-currN.Output)**2
            currN.eps=Expected[i]-currN.Output
        self.OutputLayer.Propagate()
        for i in reversed(self.HiddenLayers):
                i.Propagate()
        self.InputLayer.Propagate()


print("Brain class imported")
