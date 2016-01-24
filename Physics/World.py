# author: b8horpet


from Physics.Basics import *


from Physics.Object import *
from Physics.Creature import *


class World:
    def __init__(self):
        """
        ... and the programmer called the constructor, and there was World
        """
        self.Objects = []
        self.Creatures = []
        self.tkp=None
        self.dtkp=None

    def Physics(self, dT: float) -> None:
        for o in self.Objects:
            o.Physics(dT)
        colls=[]
        for i in range(0,len(self.Objects)):
            for j in range(i+1,len(self.Objects)):
                if self.Objects[i].Collide(self.Objects[j]) == True:
                    colls.append((self.Objects[i],self.Objects[j]))
        colleffs=[]
        for o,p in colls:
            oc=o.DoCollision(p)
            pc=p.DoCollision(o)
            colleffs.append(((o,oc),(p,pc)))
        for (o,oc),(p,pc) in colleffs:
            o.Pos+=oc[0]
            o.Vel+=oc[1]
            o.Acc+=oc[2]
            p.Pos+=pc[0]
            p.Vel+=pc[1]
            p.Acc+=pc[2]
        for c in self.Creatures:
            c.Logic()

    def GetRenderData(self):
        for i in range(0,5):
            self.Physics(0.01) # should not be here
        pos = []
        siz = []
        col = []
        # Surface2D for now
        tkp=Vector3D()
        mt=0.0
        for o in self.Objects:
            pos.append((o.Pos.x, o.Pos.y))
            tkp+=o.Mass*o.Pos
            mt+=o.Mass
            siz.append(o.Radius)
            if type(o) == Creature:
                col.append((1,0,0,1))
            else:
                col.append((0,1,0,1))
        tkp/=mt
        if self.tkp != None:
            if self.dtkp != None:
                if abs(abs(self.tkp-tkp)-self.dtkp)>0.001:
                    print("impulse fucked")
                    self.dtkp=abs(self.tkp-tkp)
            else:
                self.dtkp=abs(self.tkp-tkp)
        self.tkp=tkp
        pos.append((tkp.x,tkp.y))
        siz.append(0.1)
        col.append((0,0,1,1))
        return pos,siz,col


print("    World class imported")
