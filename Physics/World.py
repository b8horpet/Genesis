# author: b8horpet


from Physics.Basics import *


from Physics.Object import *
from Physics.Creature import *
import cProfile, pstats


def ConstantFrics(p: Vector3D) -> float:
    return 0.05,0.3


class World:
    class Geometry:
        def __init__(self):
            self.UpdateFrics=ConstantFrics

    def __init__(self):
        """
        ... and the programmer called the constructor, and there was World
        """
        self.Objects = []
        self.Creatures = []
        self.ObjLimit=50
        self.Size=25.0
        self.Geometry = World.Geometry()
        if DEBUG:
            self.tkp=None
            self.dtkp=None

    def AddObject(self,o):
        self.Objects.append(o)
        if type(o) == Creature:
            self.Creatures.append(o)

    def RemoveObject(self,o):
        self.Objects.remove(o)
        if type(o) == Creature:
            self.Creatures.remove(o)

    def Physics(self, dT: float) -> None:
        dead=[]
        for o in self.Objects:
            if o.Alive:
                o.Frics=self.Geometry.UpdateFrics(o.Pos)
                o.Physics(dT)
            else:
                dead.append(o)
        for d in dead:
            self.RemoveObject(d)
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

    def Logic(self):
        for c in self.Creatures:
            ps=c.Pos
            mx=100.0
            for oj in self.Objects:
                if c is oj:
                    continue
                if abs(ps-oj.Pos)<mx:
                    mx=abs(ps-oj.Pos)
                    c.Organs[0].Pos=oj.Pos
            c.Logic()

    def Activate(self):
        if len(self.Objects)<self.ObjLimit:
            r=np.random.uniform(0.0,100.0)
            if r < 10:
                if r < 0.5:
                    o=Creature()
                else:
                    o=Food()
                o.Pos=Vector3D(np.random.uniform(-self.Size,self.Size),np.random.uniform(-self.Size,self.Size))
                self.AddObject(o)
        for i in range(0,5):
            self.Physics(0.01)
        self.Logic()

    def GetRenderData(self):
        if PROFILE:
            pr = cProfile.Profile()
            pr.enable()
        self.Activate()
            #cProfile.run('theWorld.Activate()')
        if PROFILE:
            pr.disable()
            sortby = 'cumulative'
            ps = pstats.Stats(pr).sort_stats(sortby)
            ps.print_stats()

        pos = []
        siz = []
        col = []
        # Surface2D for now
        if DEBUG:
            tkp=Vector3D()
            mt=0.0
        for o in self.Objects:
            pos.append((o.Pos.x, o.Pos.y))
            if DEBUG:
                tkp+=o.Mass*o.Pos
                mt+=o.Mass
            siz.append(o.Radius)
            col.append(o.Color)
        if DEBUG:
            if mt>0.0:
                tkp/=mt
                if self.tkp != None:
                    if self.dtkp != None:
                        if abs(abs(self.tkp-tkp)-self.dtkp)>0.001:
                            #print("momentum fucked")
                            self.dtkp=abs(self.tkp-tkp)
                    else:
                        self.dtkp=abs(self.tkp-tkp)
                self.tkp=tkp
                pos.append((tkp.x,tkp.y))
                siz.append(0.1)
                col.append((0,0,1,1))
        return pos,siz,col


print("    World class imported")
