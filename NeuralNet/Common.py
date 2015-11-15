__author__ = 'b8horpet'


class PureVirtualCallException(Exception):
    pass


class NeuralObjectInterface:
    def __init__(self):
        raise PureVirtualCallException

    def __del__(self):
        raise PureVirtualCallException

    def Activate(self):
        raise PureVirtualCallException

