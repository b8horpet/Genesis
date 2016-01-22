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

    def Physics(self, dT: float) -> None:
        for o in self.Objects:
            o.Physics(dT)
        #for c in self.Creatures:
        #    c.Physics(dT)

    def GetRenderData(self):
        self.Physics(0.05) # should not be here
        pos = []
        siz = []
        col = []
        # Surface2D for now
        for o in self.Objects:
            pos.append((o.Pos.x, o.Pos.y))
            siz.append((o.Radius*20)**2)
            if type(o) == Creature:
                col.append((1,0,0,1))
            else:
                col.append((0,1,0,1))
        #for c in self.Creatures:
        #    pos.append((c.Pos.x, c.Pos.y))
        #    siz.append(100)
        #    col.append((0,1,0,1))
        return pos,siz,col


print("    World class imported")
