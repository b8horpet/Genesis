#author: b8horpet


from Physics.Basics import *


class Object:
    """
    Simulation of real world objects
    """
    class Effect:
        def __init__(self):
            raise NotImplementedError()

    ID=0
    NumColls=0
    NumCollTests=0

    def __init__(self):
        Object.ID+=1
        self.ID=Object.ID

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

    def GetBoundingBox(self):
        """
        Returns the topleft and bottomright corner of the bounding box
        """
        raise NotImplementedError()

class Sphere(Object):
    class PhysEffect(Object.Effect):
        def __init__(self, p=Vector3D(), v=Vector3D(), a=Vector3D(), m=0.0, r=0.0):
            self.dP=p
            self.dV=v
            self.dA=a
            self.dM=m
            self.dR=r

    def __init__(self, p=Vector3D()):
        super(Sphere,self).__init__()
        self.Mass = 1.0
        self.Radius = 0.5
        self.Pos=Vector3D(p.x,p.y,p.z) # must be inside of the Object
        self.Vel=Vector3D()
        self.Acc=Vector3D()
        self.Frics=0.0,0.0 # first is linear second is quadratic (like in water)
        self.Color=(1,1,1,1)
        self.Alive=True
        #might be better to store prev pos, than acceleration

    def Physics(self, dT: float):
        self.Eulerish(dT)
        #self.RK4(dT)

    def Eulerish(self, dT: float):
        ad=Vector3D(0.0,0.0,0.0)
        for c in enumerate(self.Frics):
            ad+=-1*c[1]*(abs(self.Vel)**c[0])*self.Vel
        ad/=self.Mass
        self.Acc+=ad
        self.Pos+=dT*self.Vel+((dT**2)/2)*self.Acc
        self.Vel+=dT*self.Acc
        self.Acc=Vector3D(0.0,0.0,0.0)

    def RK4(self, dT: float):
        ad=Vector3D(0.0,0.0,0.0)
        for c in enumerate(self.Frics):
            ad+=-1*c[1]*(abs(self.Vel)**c[0])*self.Vel
        ad/=self.Mass
        self.Acc+=ad
        # acceleration should be computed again in the steps
        k1=(dT*self.Vel,dT*self.Acc)
        k2=(dT*(self.Vel+0.5*k1[0]),dT*(self.Acc+0.5*k1[1]))
        k3=(dT*(self.Vel+0.5*k2[0]),dT*(self.Acc+0.5*k2[1]))
        k4=(dT*(self.Vel+k3[0]),dT*(self.Acc+k3[1]))
        self.Pos+=(1.0/6.0)*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        self.Vel+=(1.0/6.0)*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        self.Acc=Vector3D(0.0,0.0,0.0)

    def Collide(self, other):
        Object.NumCollTests+=1
        rad_sum=self.Radius+other.Radius
        pos_diff=self.Pos-other.Pos
        if abs(pos_diff.x) > rad_sum or abs(pos_diff.y) > rad_sum:
            return False
        return pos_diff*pos_diff < rad_sum**2

    def DoCollision(self, other):
        Object.NumColls+=1
        #todo WTF
        d=self.Pos-other.Pos
        d/=abs(d)
        vtkp=(self.Mass*self.Vel+other.Mass*other.Vel)/(self.Mass+other.Mass)
        v1=other.Vel-vtkp
        vm=(v1*d)*d
        vp=v1-vm
        vcorr=vp-vm
        vcorr+=vtkp

        pcorr=-1.0*d
        dd=self.Radius+other.Radius
        dd-=abs(other.Pos-self.Pos)
        dd*=self.Mass
        dd/=(other.Mass+self.Mass)
        pcorr*=dd
        vcorr-=other.Vel
        acorr=Vector3D()
        return Sphere.PhysEffect(pcorr,vcorr,acorr)

    def DoEffect(self, e):
        self.Pos+=e.dP
        self.Vel+=e.dV
        self.Acc+=e.dA
        self.Mass+=e.dM
        self.Radius+=e.dR

    def GetBoundingBox(self):
        return self.Pos-Vector3D(self.Radius,self.Radius,self.Radius), self.Pos+Vector3D(self.Radius,self.Radius,self.Radius)