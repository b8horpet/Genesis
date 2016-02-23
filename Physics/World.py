# author: b8horpet


from Physics.Basics import *


from Physics.Object import *
from Physics.Creature import *
import cProfile, pstats
import pickle


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

        def BuildTiles(self, os):
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

        def DoCollisions(self):
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



    def __init__(self, random):
        """
        ... and the programmer called the constructor, and there was World
        """

        self.Random = random
        self.Objects = []
        self.Creatures = []
        self.ObjLimit=50
        self.Size=25.0
        self.TickCnt=0
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
        self.Geometry.BuildTiles(self.Objects)
        self.Geometry.DoCollisions()

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
        for i in range(0,5):
            self.TickCnt+=1
            self.TickCnt%=5
            if self.TickCnt == 1:
                self.Spawn()
            self.Physics(0.01)
            if self.TickCnt == 0:
                self.Logic()

    def Dump(self):
        l=[]
        for o in self.Objects:
            l.append((type(o),o.Pos.x,o.Pos.y))
        return pickle.dumps(l)

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
