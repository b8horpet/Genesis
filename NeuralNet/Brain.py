#author: b8horpet


from NeuralNet.Common import *
from NeuralNet.Neuron import *
import numpy as np


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

    def RegisterNeuron(self, n):
        if type(n)==InputNeuron:
            self.InputLayer.Neurons.append(n)
        elif type(n)==OutputNeuron:
            self.OutputLayer.Neurons.append(n)
        else:
            raise Exception() #wtf?

    def FillSynapsisGraph(self, random):
        l=len(self.HiddenLayers)
        if l>0:
            for i in self.InputLayer.Neurons:
                for o in self.HiddenLayers[0].Neurons:
                    Synapsis(i,o,random.uniform(-1,1))
            for h in range(0,l-1):
                for i in self.HiddenLayers[h].Neurons:
                    for o in self.HiddenLayers[h+1].Neurons:
                        Synapsis(i,o,random.uniform(-1,1))
            for i in self.HiddenLayers[l-1].Neurons:
                for o in self.OutputLayer.Neurons:
                    Synapsis(i,o,random.uniform(-1,1))
        else:
            for i in self.InputLayer.Neurons:
                for o in self.OutputLayer.Neurons:
                    Synapsis(i,o,random.uniform(-1,1))

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


print("    Brain class imported")
