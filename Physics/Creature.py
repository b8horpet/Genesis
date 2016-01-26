#author: b8horpet


from Physics.Basics import *
from Physics.Object import *
from NeuralNet import *
import numpy as np


class Creature(Sphere): # one cell, spheric (for now)
    class Organ:
        def __init__(self,p):
            self.Parent=p

        def Activate(self):
            pass

    class Sensor(Organ):
        def __init__(self,p,nx,ny):
            super(Creature.Sensor,self).__init__(p)
            self.NeuronX=nx
            self.NeuronY=ny
            self.Pos=None

        def Activate(self):
            if self.Parent.Energy > 0.0:
                if self.Pos != None:
                    d=self.Parent.Pos-self.Pos
                    d.Normalize()
                    self.NeuronX.Inputs[0]=d.x
                    self.NeuronY.Inputs[0]=d.y
                    self.Pos=None
                self.Parent.Energy-=0.01

    class Motor(Organ):
        def __init__(self,p,nx,ny):
            super(Creature.Motor,self).__init__(p)
            self.NeuronX=nx
            self.NeuronY=ny


        def Activate(self):
            if self.Parent.Energy > 0.0:
                self.Parent.Acc.x-=self.NeuronX.Output/10.0
                self.Parent.Acc.y-=self.NeuronY.Output/10.0
                for f in self.Parent.Frics:
                    self.Parent.Energy-=f*0.1

    def __init__(self):
        super(Creature,self).__init__()
        self.Energy=1000.0
        self.Health=100.0
        self.Color=(np.random.uniform(0.0,0.3),np.random.uniform(0.2,0.8),np.random.uniform(0.0,0.3),1)
        self.Brain=Brain()
        ix=InputNeuron()
        iy=InputNeuron()
        ox=OutputNeuron()
        oy=OutputNeuron()
        self.Brain.InputLayer.Neurons.append(ix)
        self.Brain.InputLayer.Neurons.append(iy)
        self.Brain.OutputLayer.Neurons.append(ox)
        self.Brain.OutputLayer.Neurons.append(oy)
        Synapsis(ix,ox,1.0)
        Synapsis(ix,oy,0.0)
        Synapsis(iy,ox,0.0)
        Synapsis(iy,oy,1.0)
        s=Creature.Sensor(self,ix,iy)
        m=Creature.Motor(self,ox,oy)
        self.Organs=[s,m]

    def Physics(self, dT: float):
        for o in self.Organs:
            o.Activate()
        super(Creature,self).Physics(dT)
        if self.Energy<100.0:
            self.Health-=0.1
        if self.Health<=0.0:
            self.Color = (1,0,0,1)
            self.Energy-=1.0
            if self.Energy < -1000.0:
                self.Alive=False

    def DoCollision(self, other):
        if type(other) != Food:
            self.Health-=1.0
        return super(Creature,self).DoCollision(other)

    def Logic(self):
        if self.Energy > 0.0:
            self.Brain.Activate()
            self.Energy-=0.05


class Food(Sphere):
    def __init__(self):
        super(Food,self).__init__()
        self.Nutrient=100.0
        self.Radius=0.1
        self.Mass=0.1
        self.Color=(1,1,0,1)

    def DoCollision(self, other):
        if type(other) == Creature:
            if other.Health > 0.0:
                other.Energy+=self.Nutrient
                self.Nutrient=0.0
                self.Alive=False
        return super(Food,self).DoCollision(other)