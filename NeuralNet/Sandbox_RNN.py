import sys,os,inspect
sys.path.append((os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))+"/..")
import NeuralNet
import numpy as np

def hash_word(w):
    m=1
    r=0
    for i in w:
        r+=i/m
        m*=128
    return r

print(hash_word(b"aaa"))
sys.exit(0)

RNN=NeuralNet.Brain()
RNN.HiddenLayers.append(NeuralNet.NeuronLayer())
RNN.InputLayer.Neurons.append(NeuralNet.InputNeuron())
RNN.OutputLayer.Neurons.append(NeuralNet.OutputNeuron())
RNN.HiddenLayers[0].Neurons.append(NeuralNet.RecurrentNeuron())
RNN.FillSynapsisGraph(np.RandomState(seed=0))

