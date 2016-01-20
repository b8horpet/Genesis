# author: b8horpet


from Physics.Basics import *


# from Physics.Object import *
# from Physics.Creature import *


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
        for c in self.Creatures:
            c.Physics(dT)

    def GetRenderData(self) -> list:
        self.Physics(0.05) # should not be here
        d = []
        # Surface2D for now
        for o in self.Objects:
            d.append((o.Pos.x, o.Pos.y))
        for c in self.Creatures:
            d.append((c.Pos.x, c.Pos.y))
        return d


print("    World class imported")
