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


print("Brain class imported")
