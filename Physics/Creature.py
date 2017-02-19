#author: b8horpet


from Physics.Basics import *
from Physics.Object import *
from NeuralNet import *
import numpy as np


class Creature(Sphere): # one cell, spheric (for now)
    class Interact(Sphere.PhysEffect):
        def __init__(self, ph):
            super(Creature.Interact,self).__init__(ph.dP,ph.dV,ph.dA)
            self.dE=0.0
            self.dH=0.0
            self.Kill=False

    class Organ:
        def __init__(self,p):
            self.Parent=p

        def Activate(self):
            pass

        def IsInput(self):
            return False

        def IsOutput(self):
            return False

    class Sensor(Organ):
        def __init__(self,p):
            super(Creature.Sensor,self).__init__(p)
            self.Radius=10.0
            self.NeuronX=InputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronX)
            self.NeuronY=InputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronY)
            self.NeuronP=InputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronP)
            self.NeuronC=InputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronC)
            self.NeuronS=InputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronS)
            self.Pos=None
            self.Dist=0.0
            self.Color=(0,0,0,0)
            self.Size=0.0

        def IsInput(self):
            return True

        def Reset(self):
            self.Pos=None
            self.Dist=0.0
            self.Color=(0,0,0,0)
            self.Size=0.0

        def UpdateTarget(self,o):
            if o == None:
                self.Reset()
                return
            rad_sum=self.Radius+o.Radius
            pos_diff=self.Parent.Pos-o.Pos
            if abs(pos_diff.x) > rad_sum or abs(pos_diff.y) > rad_sum:
                return
            pd2=pos_diff*pos_diff
            if pd2 < rad_sum**2:
                if self.Pos == None or self.Dist*self.Dist>pd2:
                    self.Pos=o.Pos
                    self.Dist=np.sqrt(pd2)
                    self.Color=o.Color
                    self.Size=o.Radius

        def Activate(self):
            if self.Parent.IsAlive():
                if self.Pos != None:
                    d=self.Parent.Pos-self.Pos
                    d.Normalize()
                    self.NeuronX.Inputs[0]=d.x
                    self.NeuronY.Inputs[0]=d.y
                    self.NeuronP.Inputs[0]=10/(1+self.Dist)
                    cavg=self.Color[0]+self.Color[1]+self.Color[2]
                    cavg*=2/3.0
                    cavg-=1.0
                    self.NeuronC.Inputs[0]=cavg
                    self.NeuronS.Inputs[0]=self.Size
                    self.Parent.Energy-=0.05
                else:
                    self.NeuronX.Inputs[0]=0.0
                    self.NeuronY.Inputs[0]=0.0
                    self.NeuronC.Inputs[0]=0.0
                    self.NeuronS.Inputs[0]=0.0
                    self.NeuronP.Inputs[0]=0.0


    class Motor(Organ):
        def __init__(self,p):
            super(Creature.Motor,self).__init__(p)
            self.NeuronX=OutputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronX)
            self.NeuronY=OutputNeuron()
            self.Parent.Brain.RegisterNeuron(self.NeuronY)

        def IsOutput(self):
            return True

        def Activate(self):
            if self.Parent.IsAlive():
                self.Parent.Acc.x-=self.NeuronX.Output
                self.Parent.Acc.y-=self.NeuronY.Output
                for f in self.Parent.Frics:
                    self.Parent.Energy-=f*0.2



    def __init__(self, p=Vector3D()):
        super(Creature,self).__init__(p)

        # seed or random may have to come from outside later
        self.Random = np.random.RandomState(seed=self.ID)

        self.Energy=300.0
        self.Health=100.0
        self.Color=(self.Random.uniform(0.0, 0.3),
                    self.Random.uniform(0.2, 0.8),
                    self.Random.uniform(0.0, 0.3),
                    1)
        self.Brain=None
        self.Organs=[]
        self.SetupBrain()

    def SetupBrain(self):
        self.Brain=Brain()
        s=Creature.Sensor(self)
        m=Creature.Motor(self)
        self.Organs.append(s)
        self.Organs.append(m)
        #ix=self.Brain.InputLayer.Neurons[0]
        #iy=self.Brain.InputLayer.Neurons[1]
        #ox=self.Brain.OutputLayer.Neurons[0]
        #oy=self.Brain.OutputLayer.Neurons[1]
        #Synapsis(ix,ox,1.0)
        #Synapsis(ix,oy,0.0)
        #Synapsis(iy,ox,0.0)
        #Synapsis(iy,oy,1.0)

        nhl=2
        for i in range(0,nhl):
            self.Brain.HiddenLayers.append(NeuronLayer())
            nhn=10
            for j in range(0,nhn):
                self.Brain.HiddenLayers[i].Neurons.append(HiddenNeuron())
        self.Brain.FillSynapsisGraph(self.Random)

    def UpdateInputs(self,o):
        for i in self.Organs:
            if i.IsInput():
                i.UpdateTarget(o)

    def Physics(self, dT: float):
        for o in self.Organs:
            o.Activate()
        if self.Energy<100.0 and self.Health > 0.0:
            self.Health-=0.5
            self.Energy+=5.0
        elif self.Energy>1000.0 and self.Health < 95.0:
            self.Energy-=20.0
            self.Health+=1.0
        if self.Health<=0.0:
            self.Mass=0.1
            if self.Energy > 0:
                self.Color=(1,1,0,1)
            else:
                self.Color=(1,0,0,1)
            self.Energy-=0.5
            if self.Energy < -1000.0:
                self.Alive=False
        super(Creature,self).Physics(dT)

    def DoCollision(self, other):
        e = Creature.Interact(super(Creature,self).DoCollision(other))
        if type(other) == Food:
            pass # food does the job
        elif type(other) == Creature:
            if other.Health <= 0.0:
                if self.IsAlive():
                    e.dE-=other.Energy
                    e.Kill=True
            elif other.Energy > 0.0:
                e.dE-=5.0
            if self.Health <= 0.0:
                if other.IsAlive():
                    e.dE+=self.Energy/10
            elif self.Energy > 0.0:
                e.dH-=self.Energy/100 # and they bite
            else:
                pass # they are soft, do not deal damage from collision
        else:
            pass
            #self.Health-=1.0 # hm, haven't thought of this
        return e

    def Logic(self):
        if self.IsAlive():
            self.Brain.Activate()
            self.Energy-=0.05

    def DoEffect(self, e):
        self.Energy+=e.dE
        self.Health+=e.dH
        if e.Kill:
            self.Alive=False
        super(Creature,self).DoEffect(e)

    def IsAlive(self):
        return self.Health>0.0 and self.Energy>0.0


class Food(Sphere):
    def __init__(self):
        super(Food,self).__init__()
        self.Nutrient=200.0
        self.Radius=0.1
        self.Mass=0.1
        self.Color=(1,1,0,1)

    def Physics(self, dT: float):
        self.Nutrient-=dT*10
        if self.Nutrient<=0.0:
            self.Alive=False
        super(Food,self).Physics(dT)

    def DoCollision(self, other):
        e=Creature.Interact(super(Food,self).DoCollision(other))
        if type(other) == Creature:
            if other.IsAlive():
                e.dE=self.Nutrient
                self.Nutrient=0.0
                self.Alive=False
        return e

class Obstacle(Sphere):
    def __init__(self,p=Vector3D):
        super(Obstacle,self).__init__(p)
        self.Damage=10.0
        #self.Radius=3.0
        self.Radius = 2.0
        self.Mass=10.0
        self.Color=(0.2,0.2,0.2,1)

    def DoCollision(self, other):
        e=Creature.Interact(super(Obstacle,self).DoCollision(other))
        if type(other) == Creature:
            if other.Health > 0.0:
                e.dH=-self.Damage
        return e