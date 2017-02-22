# author: b8horpet


from Physics.Basics import *


from Physics.Object import *
from Physics.Creature import *
import cProfile, pstats
import pickle
from functools import partial


def ConstantFrics(p: Vector3D) -> float:
    return 0.05,0.3


class World:
    class Tile:
        def __init__(self, x: int, y: int):
            self.x=x
            self.y=y
            self.count=0
            self.Objects=[]

        def AddObject(self, o):
            self.count+=1
            self.Objects.append(o)

        def Collide(self):
            if self.count == 1:
                return set()
            colls=set()
            for i in range(0,len(self.Objects)):
                for j in range(i+1,len(self.Objects)):
                    if self.Objects[i].Collide(self.Objects[j]) == True:
                        colls.add((self.Objects[i],self.Objects[j]))
            return colls

    class Geometry:
        def __init__(self):
            self.UpdateFrics=ConstantFrics
            self.TileSize=5
            self.Tiles={}

        def GetTile(self, x: float, y: float):
            tx=int(np.floor(x))//self.TileSize
            ty=int(np.floor(y))//self.TileSize
            if (tx,ty) not in self.Tiles:
                self.Tiles[(tx,ty)]=World.Tile(tx,ty)
            return self.Tiles[(tx,ty)]

        def DoCollisions(self, os):
            self.BroadPhase(os)
            self.NarrowPhase()

        def BroadPhase(self, os):
            self.Tiles={} # sry gc
            for o in os:
                t=self.GetTile(o.Pos.x,o.Pos.y)
                t.AddObject(o)
                additional={}
                if t.x*self.TileSize>o.Pos.x-o.Radius:
                    self.GetTile(o.Pos.x-o.Radius,o.Pos.y).AddObject(o)
                    additional['x']=0
                if (t.x+1)*self.TileSize<o.Pos.x+o.Radius:
                    self.GetTile(o.Pos.x+o.Radius,o.Pos.y).AddObject(o)
                    additional['x']=1
                if t.y*self.TileSize>o.Pos.y-o.Radius:
                    self.GetTile(o.Pos.x,o.Pos.y-o.Radius).AddObject(o)
                    additional['y']=0
                if (t.y+1)*self.TileSize<o.Pos.y+o.Radius:
                    self.GetTile(o.Pos.x,o.Pos.y+o.Radius).AddObject(o)
                    additional['y']=1
                if len(additional) == 2:
                    corner=Vector3D(t.x+additional['x'],t.y+additional['y'])
                    corner*=self.TileSize
                    if abs(corner-o.Pos)<o.Radius:
                        cx=corner.x+additional['x']*2-1
                        cy=corner.y+additional['y']*2-1
                        self.GetTile(cx,cy).AddObject(o)

        def NarrowPhase(self):
            colls=set()
            for p in self.Tiles:
                colls.update(self.Tiles[p].Collide())
            colleffs=[]
            for o,p in colls:
                oc=o.DoCollision(p)
                pc=p.DoCollision(o)
                colleffs.append(((o,oc),(p,pc)))
            for (o,oc),(p,pc) in colleffs:
                o.DoEffect(pc)
                p.DoEffect(oc)

    class Geometry_RDC:
        def __init__(self):
            self.UpdateFrics=ConstantFrics
            self.TileSize=5
            self.Clusters=[]

        def DoCollisions(self, os):
            self.BroadPhase(os)
            self.NarrowPhase()

        def get_pos_by_dim(d, v):
            return getattr(v.GetBoundingBox()[0],d)

        def BroadPhase(self, os):
            self.Clusters=[]
            #could be done on separate threads
            dimensions=['x','y'] # only 2 dimension
            #this is fragile, should be indexed with numbers
            dirtyClusters=[[os,[True for d in dimensions]]]
            dim=0
            while dirtyClusters:
                dc=dimensions[dim]
                #print("pass %s %d" % (dc,len(dirtyClusters)))
                for i in reversed(range(len(dirtyClusters))):
                    c=dirtyClusters.pop(i)
                    if True not in c[1]:
                        self.Clusters.append(c[0])
                        continue
                    if not c[0]:
                        c[1][dim]=False
                        continue
                    c[0].sort(key=partial(World.Geometry_RDC.get_pos_by_dim,dc))
                    clusterBoundaries=[]
                    maxD=getattr(c[0][0].GetBoundingBox()[0],dc)
                    for j,o in enumerate(c[0]):
                        bb=o.GetBoundingBox()
                        od_r=getattr(bb[1],dc)
                        od_l=getattr(bb[0],dc)
                        if od_l > maxD:
                            clusterBoundaries.append(j)
                            maxD=od_r
                        elif od_r > maxD:
                            maxD=od_r
                    if not clusterBoundaries:
                        c[1][dim]=False
                        dirtyClusters.append(c)
                    else:
                        clusterBoundaries.append(len(c[0]))
                        lastbound=0
                        for j in clusterBoundaries:
                            dirtyClusters.append([c[0][lastbound:j],[x!=dim for x in range(len(dimensions))]])
                            lastbound=j
                dim+=1
                dim%=len(dimensions)

        def NarrowPhase(self):
            for c in self.Clusters:
                for i in range(len(c)-1):
                    o1=c[i]
                    for j in range(i+1,len(c)):
                        o2=c[j]
                        colls=[]
                        if o1.Collide(o2) == True:
                            colls.append((o1,o2))
                        colleffs=[]
                        for o,p in colls:
                            oc=o.DoCollision(p)
                            pc=p.DoCollision(o)
                            colleffs.append(((o,oc),(p,pc)))
                        for (o,oc),(p,pc) in colleffs:
                            o.DoEffect(pc)
                            p.DoEffect(oc)


    def __init__(self, random):
        """
        ... and the programmer called the constructor, and there was World
        """

        self.Random = random
        self.Objects = []
        self.Creatures = []
        self.ObjLimit=1000
        self.Size=25.0
        self.TickCnt=0
        self.Geometry = World.Geometry()
        #self.Geometry = World.Geometry_RDC()
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
        self.Geometry.TileSize=0.0
        for o in self.Objects:
            if o.Alive:
                o.Frics=self.Geometry.UpdateFrics(o.Pos)
                if self.Geometry.TileSize<o.Radius:
                    self.Geometry.TileSize=o.Radius
                o.Physics(dT)
            else:
                dead.append(o)
        for d in dead:
            self.RemoveObject(d)
        self.Geometry.TileSize*=2.0
        self.Geometry.TileSize=int(np.round(self.Geometry.TileSize))+1
        self.Geometry.DoCollisions(self.Objects)

    def Logic(self):
        for c in self.Creatures:
            c.UpdateInputs(None)
            for oj in self.Objects:
                if c is oj:
                    continue
                c.UpdateInputs(oj)
            c.Logic()

    def Spawn(self):
        if len(self.Objects)<self.ObjLimit:
            r=self.Random.uniform(0.0, 100.0)
            if r < 10:
                o=Food()
                o.Pos=Vector3D(self.Random.uniform(-self.Size, self.Size), self.Random.uniform(-self.Size, self.Size))
                self.AddObject(o)


    def Activate(self):
        if PROFILE:
            pr = cProfile.Profile()
            pr.enable()
        for i in range(0,5):
            self.TickCnt+=1
            self.TickCnt%=5
            if self.TickCnt == 1:
                self.Spawn()
            self.Physics(0.01)
            if self.TickCnt == 0:
                self.Logic()
        if PROFILE:
            pr.disable()
            sortby = 'cumulative'
            ps = pstats.Stats(pr).sort_stats(sortby)
            ps.print_stats()

    def Dump(self):
        l=[]
        for o in self.Objects:
            l.append((type(o),o.Pos.x,o.Pos.y))
        return pickle.dumps(l)

    def GetRenderData(self):
        self.Activate()
            #cProfile.run('theWorld.Activate()')

        pos = []
        siz = []
        col = []
        txt = []
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
            if type(o) == Creature:
                txt.append("%3.3f %4.3f" % (o.Health, o.Energy))
            else:
                txt.append("")
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
        return pos,siz,col,txt


print("    World class imported")
