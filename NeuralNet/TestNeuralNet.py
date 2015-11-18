import unittest

from NeuralNet import *


class TestNeuron(unittest.TestCase):
    def test_PureVirtual(self):
        """
        The base interface of all neural object should lack implementatiom.
        It is an abstract class. Cannot be initiated.
        """
        with self.assertRaises(PureVirtualCallException):
            n=NeuralObjectInterface()

    def test_SignalTransferSpeed(self):
        """
        The synapses should not delay the signal transfer.
        The input should go through the whole network in one tick.
        """
        b=Brain()
        b.InputLayer.Neurons.append(InputNeuron())
        b.HiddenLayers.append(NeuronLayer())
        b.HiddenLayers[0].Neurons.append(HiddenNeuron())
        b.HiddenLayers.append(NeuronLayer())
        b.HiddenLayers[1].Neurons.append(HiddenNeuron())
        b.OutputLayer.Neurons.append(OutputNeuron())
        Synapsis(b.InputLayer.Neurons[0],b.HiddenLayers[0].Neurons[0])
        Synapsis(b.HiddenLayers[0].Neurons[0],b.HiddenLayers[1].Neurons[0])
        Synapsis(b.HiddenLayers[1].Neurons[0],b.OutputLayer.Neurons[0])
        x=3.14159265358979
        b.InputLayer.Neurons[0].GetInput=ConstValueHolder(x)
        b.Activate()
        self.assertEqual(b.OutputLayer.Neurons[0].Output,x)

    def test_Functions(self):
        self.assertGreater(len(Derivatives),0)
        fxsqrd=Polinomial(2)
        self.assertTrue(fxsqrd in Derivatives)
        fxm2=Polinomial(1,2.0)
        self.assertFalse(fxm2 in Derivatives)


if __name__ == '__main__':
    unittest.main()

