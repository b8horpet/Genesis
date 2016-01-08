#author: b8horpet


from Physics.Basics import *


class Object:
    """
    Simulation of real world objects
    """
    def __init__(self):
        raise NotImplementedError()

    def Physics(self, dT: float):
        """
        Compute next state based on current state
        """
        raise NotImplementedError()

    def Collide(self, other):
        """
        Compute collision or possible interaction with other object
        """
        raise NotImplementedError()

class Sphere(Object):
    def __init__(self):
        self.Mass = 1.0
        self.Radius = 1.0
        self.Pos=Vector3D() # must be inside of the Object
        self.Vel=Vector3D()
        self.Acc=Vector3D()
        #might be better to store prev pos, than acceleration

    def Physics(self, dT: float):
        self.Pos+=dT*self.Vel+((dT**2)/2)*self.Acc
        self.Vel+=dT*self.Acc
        self.Acc=0.0

    def Collide(self, other):
        if hasattr(self,'reentry'):
            delattr(self,'reentry')
            return None
        self.reentry=False
        #do magic
        if isinstance(other,Sphere):
            retVal1 = abs(self.Pos-other.Pos)<(self.Radius+other.Radius)
        else:
            retVal1 = abs(self.Pos-other.Pos)<self.Radius
        retVal2 = other.Collide(self)
        if retVal1 or retVal2: # handle None
            retVal=True
        else:
            retVal=False
        if hasattr(self,'reentry'):
            delattr(self,'reentry')
        return retVal
