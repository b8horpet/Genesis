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
        Compute collision with other object
        """
        raise NotImplementedError()

    def DoCollision(self, other):
        """
        Handles the collision with the other object
        """
        raise NotImplementedError()

class Sphere(Object):
    def __init__(self):
        self.Mass = 1.0
        self.Radius = 0.5
        self.Pos=Vector3D() # must be inside of the Object
        self.Vel=Vector3D()
        self.Acc=Vector3D()
        self.Frics=0.0,0.0
        #might be better to store prev pos, than acceleration

    def Physics(self, dT: float):
        ad=Vector3D(0.0,0.0,0.0)
        for c in enumerate(self.Frics):
            ad+=-1*c[1]*(abs(self.Vel)**c[0])*self.Vel
        ad/=self.Mass
        self.Acc+=ad
        self.Pos+=dT*self.Vel+((dT**2)/2)*self.Acc
        self.Vel+=dT*self.Acc
        self.Acc=Vector3D(0.0,0.0,0.0)

    def Collide(self, other):
        #todo WTF?
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

    def DoCollision(self, other):
        #todo WTF
        pcorr=self.Pos
        vcorr=(self.Mass*self.Vel+other.Mass*other.Vel)/(self.Mass+other.Mass)
        acorr=self.Acc
        return pcorr,vcorr,acorr